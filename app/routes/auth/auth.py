from flask_login import login_user, logout_user, login_required
from app.models.user import User

from app.routes import *
from .forms import LoginForm, RegistrationForm

main = Blueprint('auth', __name__)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('user.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('user.index'))


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        user.save()
        flash('You can now login.')
        return redirect(url_for('.login'))
    return render_template('auth/register.html', form=form)