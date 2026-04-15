from flask import Blueprint, render_template

auth_bp = Blueprint('auth', __name__)

@app.route("/login")
def login():
    return render_template("auth/login.html")