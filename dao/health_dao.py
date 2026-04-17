from flask import session
from db.connection import getConnection

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

# 최신 데이터 가져오기
def getLatestHealthData():
    user_id = session.get("user_id")

    conn = getConnection()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM health_result
                WHERE user_id = %s
                ORDER BY created_at DESC
                LIMIT 1
        """, (user_id,)
    )
    healthData = cur.fetchone()

    cur.close()
    conn.close()

    if not healthData:
        return None
    
    return healthData

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