from flask import Flask, render_template
from routes.health import health_bp
from routes.auth import auth_bp
import os
from datetime import timedelta
from dao.auth_decorators import checkSignIn
from dao.health_dao import getLatestHealthData

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev_secret_key")
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=1)

# Blueprint 등록
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(health_bp, url_prefix="/health")

# 메인(대시보드) 페이지
@app.route("/")
@checkSignIn
def home():
    # 로그인한 사람의 가장 최근 검사결과
    data = getLatestHealthData()
    return render_template("index.html", page_title="Dashboard", data=data)

if __name__ == "__main__":
    app.run(debug=True)