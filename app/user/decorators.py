from functools import wraps
from flask import session, abort


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            abort(401)
        return f(*args, **kwargs)
    return decorated_function