from flask import Flask, render_template
from routes.health import health_bp
from routes.auth import auth_bp
import os
import random
from datetime import timedelta
from dao.auth_decorators import checkSignIn
from dao.health_dao import getLatestHealthData

app = Flask(__name__)

# 랜덤 팁
HEALTH_TIPS = [
    "정기적인 건강검진은 질환을 조기에 확인하는 데 큰 도움이 됩니다.",
    "검진 결과에서 '질환 의심'이나 '위험' 판정을 받았다면 즉시 추가 검사나 생활 습관 개선을 시작해야 합니다.",
    "올해 검진을 못 받았다면, 국민건강보험공단에 '전년도 미수검 추가 등록'을 신청할 수 있습니다.",
    "2026년 기준 짝수년도 출생자가 국가검진 대상자입니다.",
    "국가 기본 검진 외에 가족력, 연령, 생활 습관에 따라 암 검진(위, 대장, 간, 유방, 자궁 등)을 추가하세요.",
    "생산직/영업직/현장직 등 비사무직 근로자는 매년 건강검진을 진행할 수 있습니다.",
    "하루 30분 정도의 가벼운 걷기 운동은 혈당과 체중 관리에 도움이 됩니다.",
    "짠 음식과 과한 야식은 혈압 관리에 부담이 될 수 있습니다.",
    "규칙적인 수면과 식습관은 건강 관리의 기본입니다.",
    "규칙적인 식사는 혈당을 안정시키고 두뇌 활동을 돕습니다.",
    "흡연과 과음은 건강검진 수치에 영향을 줄 수 있으니 주의가 필요합니다."
]

@app.context_processor
def inject_health_tip():
    return {
        "health_tip": random.choice(HEALTH_TIPS)
    }

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
    (data, HEALTH_SCHEMA) = getLatestHealthData()
    return render_template("index.html", page_title="건강검진 대시보드",
                data=data, schema=HEALTH_SCHEMA
            )


if __name__ == "__main__":
    app.run(debug=True)