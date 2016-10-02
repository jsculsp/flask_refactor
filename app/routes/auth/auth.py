from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app.routes import *
from .forms import LoginForm, RegistrationForm, ChangePasswordForm
from .forms import PasswordResetRequestForm, PasswordResetForm
from ...mail.email import send_email

main = Blueprint('auth', __name__)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('homepage.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('homepage.index'))


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        user.save()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        flash('You can now login.')
        return redirect(url_for('.login'))
    return render_template('auth/register.html', form=form)


@main.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        redirect(url_for('homepage.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('homepage.index'))


@main.before_app_request
def before_request():
    if current_user.is_authenticated \
        and not current_user.confirmed \
        and request.endpoint[:5] != 'auth.' \
        and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@main.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('homepage.index'))
    return render_template('auth/unconfirmed.html')


@main.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    print('current_user.email', current_user.email, 'token', token)
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('homepage.index'))


@main.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            current_user.save()
            flash('Your password has been updated.')
            return redirect(url_for('homepage.index'))
        else:
            flash('Invalid password.')
    return render_template('auth/change_password.html', form=form)


@main.route('/reset', methods=['GET', 'Post'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('homepage.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password',
                       'auth/email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
        flash('An email with instructions to reset your password has been'
                  'sent to you.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@main.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('homepage.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('homepage.index'))
        if user.reset_password(token, form.password.data):
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('homepage.index'))
    return render_template('auth/reset_password.html', form=form)

