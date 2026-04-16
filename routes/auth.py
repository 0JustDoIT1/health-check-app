from flask import Blueprint, render_template

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/signin")
def signin():
    return render_template("auth/signin.html")
