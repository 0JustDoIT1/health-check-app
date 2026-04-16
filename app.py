from flask import Flask, render_template
from routes.health import health_bp
from routes.auth import auth_bp
import os

app = Flask(__name__)

app.secret_key=os.environ.get("SECRET_KEY", "dev_secret_key")

# Blueprint 등록
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(health_bp, url_prefix="/health")

@app.route("/")
def home():
    return render_template("index.html", page_title="Dashboard")

if __name__ == "__main__":
    app.run(debug=True)