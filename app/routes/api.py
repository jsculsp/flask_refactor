from . import *
from app.models.post import Post
from app.models.comment import Comment
import json
from flask_login import current_user

from utils import log

main = Blueprint('api', __name__)


def api_response(success, data=None, message=''):
    r = {
        'success': success,
        'data': data,
        'message': message,
    }
    return json.dumps(r, ensure_ascii=False)


@main.route('/post/<int:id>', methods=['POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = request.form
    body = form.get('body', '')
    c = Comment(body=body, post=post,
                author=current_user._get_current_object())
    if len(body) > 0:
        c.save()
        return api_response(True, data=c.json())
    else:
        return api_response(False, message=c.error_message())
