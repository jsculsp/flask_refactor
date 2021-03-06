from . import ModelMixin
from . import db
from datetime import datetime
from markdown import markdown
import bleach
from flask import render_template


class Comment(db.Model, ModelMixin):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code',
                        'em', 'i', 'strong', 'br']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def json(self):
        t = render_template('api/comment.html', comment=self)
        return t

    def error_message(self):
        if len(self.body) <= 0:
            return '评论不能为空！'

db.event.listen(Comment.body, 'set', Comment.on_changed_body)
