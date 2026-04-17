from flask import Flask, render_template
from routes.health import health_bp
from routes.auth import auth_bp
import os
from datetime import timedelta
from dao.auth_decorators import checkSignIn

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev_secret_key")
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=1)

# Blueprint 등록
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(health_bp, url_prefix="/health")

@app.route("/")
@checkSignIn
def home():
    return render_template("index.html", page_title="Dashboard")

if __name__ == "__main__":
    app.run(debug=True)