from flask import Blueprint, abort, redirect, render_template
from tinifyUrl.redis import get_redis
from tinifyUrl.constants import CODE_LENGTH


bp = Blueprint('frontend', __name__)


# User facing views.


@bp.route('/')
def main_page():
    return render_template('index.html')


@bp.route('/<string(length={}):code>'.format(CODE_LENGTH))
def forward_page(code):
    return_url = get_redis().get(code)
    if not return_url:
        abort(404)
    return_url = return_url.decode('utf-8')
    if return_url[:4] != 'http':
        return redirect('http://' + return_url, code=302)
    return redirect(return_url, code=302)
