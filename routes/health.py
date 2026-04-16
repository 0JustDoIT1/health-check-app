from flask import Blueprint, render_template, redirect, url_for

health_bp = Blueprint('health', __name__)

@health_bp.route("/")
def healthMain():
    return redirect(url_for("health.healthCheck"))

@health_bp.route("/check")
def healthCheck():
    return render_template("health/check.html", page_title="건강검진")