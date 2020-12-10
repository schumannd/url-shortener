from flask import Blueprint, request, abort
from tinifyUrl.redis import get_redis
from tinifyUrl.constants import NUM_RETRIES_ON_COLLISION, CODE_LENGTH, URL_MINIFICATION_TIMEOUT

import hashlib
import random
import string
import base62


bp = Blueprint('service', __name__)


# API views.


def string_to_code(string_to_encode):
    hash_bytes = hashlib.md5(string_to_encode.encode('utf-8')).digest()
    code_representation = base62.encodebytes(hash_bytes)
    return code_representation[:CODE_LENGTH]


def save_url_if_not_exists(url):
    string_to_encode = url
    tries = 0
    while tries < NUM_RETRIES_ON_COLLISION:
        code = string_to_code(string_to_encode)
        existing_entry = get_redis().get(code)
        if existing_entry and existing_entry.decode('utf-8') != url:
            string_to_encode += random.choice(string.ascii_letters + string.digits)
            tries += 1
        else:
            break

    if tries == NUM_RETRIES_ON_COLLISION:
        # notify monitoring service that NUM_RETRIES_ON_COLLISION collisions occurred.
        abort(400, 'Please try again later')

    get_redis().set(code, url, ex=URL_MINIFICATION_TIMEOUT, nx=True)
    return code


@bp.route('/shorten-url', methods=['POST'])
def shorten_view():
    url = request.json['url'].strip()
    return_code = save_url_if_not_exists(url)
    return {'code': return_code}


# unused
@bp.route('/expand-url', methods=['POST'])
def expand_view():
    code_to_expand = request.json['code']
    return_url = get_redis().get(code_to_expand)
    if not return_url:
        abort(404)
    return {'url': return_url.decode('utf-8')}
