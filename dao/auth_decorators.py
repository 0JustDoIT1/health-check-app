from functools import wraps
from flask import session, redirect, url_for

def checkSignIn(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.signIn"))
        return f(*args, **kwargs)
    return wrapper

def checkGuest(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" in session:
            return redirect(url_for('home'))  # 또는 dashboard
        return f(*args, **kwargs)
    return wrapper