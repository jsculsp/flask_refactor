from functools import wraps

from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import session
from flask import url_for
from flask import abort
from flask import current_app
from flask import flash
from flask import make_response

global_main = Blueprint('error', __name__)


@global_main.app_errorhandler(403)
def forbidden(e):
    return render_template('error/403.html'), 403


@global_main.app_errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404


@global_main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('error/500.html'), 500
