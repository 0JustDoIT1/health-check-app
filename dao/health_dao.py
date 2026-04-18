from flask import session
from datetime import date
from db.connection import getConnection
from constants.health import BASE_SCORE, HEALTH_SCHEMA

# 유저 기본 정보 가져오기 (id, email, name, age)
def getUser(user_id):
    conn = getConnection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, email, name, age
        FROM users
        WHERE id = %s
    """, (user_id,))

    user = cur.fetchone()
    conn.close()

    return user

# 나이 계산
def calculate_age(birth_date_str):
    birth_date = date.fromisoformat(birth_date_str)
    today = date.today()

    return today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )

# 검진 당시 나이 계산 함수
def calculate_exam_age(birth_date, exam_date):
    # 이미 date 타입이라면 변환 없이 그대로 사용
    age = exam_date.year - birth_date.year
    
    # 생일이 지나지 않았다면 나이를 한 살 뺌
    if (exam_date.month, exam_date.day) < (birth_date.month, birth_date.day):
        age -= 1
    
    return age

# 등급 계산
def getGrade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "E"
    
# 데이터 기반 점수 계산
def calculate_health_score(data, risk_rules):
    result_labels = {}
    score = BASE_SCORE

    group_penalty = {}

    for rule in risk_rules:
        item = rule["item_name"]
        category = rule.get("category")

        # 그룹 확장
        if item == "vision":
            targets = ["vision_left", "vision_right"]
        elif item == "hearing":
            targets = ["hearing_left", "hearing_right"]
        else:
            targets = [item]

        min_v = rule["min_value"]
        max_v = rule["max_value"]
        status = rule["status"]
        gender = rule["gender"]
        risk = rule["risk_level"]
        color = rule["color_hex"]

        for t in targets:
            value = data.get(t)

            if value is None:
                continue

            if gender != "all" and gender != data["gender"]:
                continue

            if min_v <= value <= max_v:
                result_labels[t] = {
                    "value": value,
                    "status": status,
                    "risk_level": risk,
                    "base_item": item,
                    "category": category,
                    "color_hex": color
                }

                # 그룹 처리
                if category and category != "NONE":
                    group_penalty[category] = max(
                        group_penalty.get(category, 0),
                        risk
                    )
                else:
                    # independent
                    score -= risk

    # 그룹 반영
    for penalty in group_penalty.values():
        score -= penalty

    grade = getGrade(score)

    return result_labels, score, grade

# 항목별 구간 설정
def get_severity(risk):
    if risk == 0:
        return "normal"
    elif risk >= -10:
        return "mild"
    elif risk >= -20:
        return "moderate"
    else:
        return "severe"

# 항목 요약 구하기
def get_category_summary(result_labels):
    category_map = {}

    # 1️⃣ 카테고리별 worst risk = max
    for info in result_labels.values():
        cat = info["category"]
        risk = info["risk_level"]

        if cat not in category_map:
            category_map[cat] = {
                "risk": risk
            }
        else:
            # 핵심: 더 큰 값이 더 위험
            category_map[cat]["risk"] = max(
                category_map[cat]["risk"],
                risk
            )

    # 2️⃣ severity 변환 (한 번만)
    for cat, data in category_map.items():
        data["status"] = get_severity(data["risk"])

    return category_map

# 정상 수치 구간 구하기
def getNormalMinMax():
    conn = getConnection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT item_name, min_value, max_value 
        FROM health_risk
        WHERE status IN ('정상', '음성')
    """)
    normal_data = cursor.fetchall()

    normal_map = {}

    for row in normal_data:
        key_name = row["item_name"]

        if key_name == "vision":
            normal_map["vision_left"] = row
            normal_map["vision_right"] = row
        elif key_name == "hearing":
            normal_map["hearing_left"] = row
            normal_map["hearing_right"] = row
        else:
            normal_map[key_name] = row

    return normal_map

# 최신 데이터 가져오기
def getLatestHealthData():
    user_id = session.get("user_id")

    conn = getConnection()
    cursor = conn.cursor()

    # 1. 최신 health_result
    cursor.execute("""
        SELECT * FROM health_result
        WHERE user_id = %s
        ORDER BY created_at DESC
        LIMIT 1
    """, (user_id,))
    
    data = cursor.fetchone()

    if not data:
        cursor.close()
        conn.close()
        return (None, HEALTH_SCHEMA)

    return (data, HEALTH_SCHEMA)

