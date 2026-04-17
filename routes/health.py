from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from db.connection import getConnection
import pymysql

health_bp = Blueprint('health', __name__)

#----------------------------------------------------------------------- #
#--------------------------------김정범-------------------------- #
# ---------------------------------------------------------------------- #

@health_bp.route("/stats/trend")
def healthTrend():
    user_id = 1 
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT created_at, weight, height, fasting_glucose, systolic_bp, diastolic_bp, ast, alt
        FROM health_result WHERE user_id = %s ORDER BY created_at ASC
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()

    trend_data = []
    for r in rows:
        h_m = r['height'] / 100
        bmi = round(r['weight'] / (h_m * h_m), 2)
        trend_data.append({
            'date': r['created_at'].strftime('%Y-%m-%d'),
            'weight': r['weight'], 'bmi': bmi, 'glucose': r['fasting_glucose']
        })
    
    # [디버깅] 터미널에 데이터가 나오는지 확인하세요!
    print(f"--- DB에서 가져온 데이터 ({len(trend_data)}건) ---")
    print(trend_data) 
    
    return render_template("health/trend.html", trend_data=trend_data)

@health_bp.route("/stats/age")
def healthAge():
    user_id = 1
    conn = getConnection()
    cursor = conn.cursor()
    # 1. 연령대별 평균 데이터
    cursor.execute("""
        SELECT FLOOR(age/10)*10 as age_group, AVG(weight) as avg_w, 
               AVG(fasting_glucose) as avg_g, AVG(systolic_bp) as avg_sbp
        FROM health_result GROUP BY FLOOR(age/10)*10 ORDER BY age_group ASC
    """)
    age_rows = cursor.fetchall()
    # 2. 내 최신 데이터와 실제 나이
    cursor.execute("SELECT age, weight, fasting_glucose FROM health_result WHERE user_id=%s ORDER BY created_at DESC LIMIT 1", (user_id,))
    my_latest = cursor.fetchone()
    conn.close()

    # 신체 나이 계산 (평균보다 낮으면 -2살 등 간단한 더미 로직)
    body_age = my_latest['age'] if my_latest else 0
    if my_latest and my_latest['weight'] < 75: body_age -= 2 

    return render_template("health/age_comp.html", 
                           age_data=age_rows, my_data=my_latest, body_age=body_age,
                           page_title="연령대별 비교")
    
#----------------------------------------------------------------------- #
#--------------------------------정다희-------------------------- #
# ---------------------------------------------------------------------- #

@health_bp.route('/create', methods=['GET', 'POST']) # route에 메서드 명시 확인!
def create_health_record():
    if request.method == 'GET':
        return render_template('health/check.html')

    # 3. DB 저장
    db = getConnection()
    cursor = db.cursor()
    
    try:
        data = {
            'user_id' : session.get("user_id"),
            'name': request.form.get('name'),
            'age': int(request.form.get('age')),
            'height': float(request.form.get('height')),
            'weight': float(request.form.get('weight')),
            'bmi': float(request.form.get('BMI')),
            'waist': float(request.form.get('waist')),
            'vision_left': float(request.form.get('vision_left')),
            'vision_right': float(request.form.get('vision_right')),
            'hearing_left': int(request.form.get('hearing_left')),
            'hearing_right': int(request.form.get('hearing_right')),
            'systolic_bp': int(request.form.get('systolic_bp')),
            'diastolic_bp': int(request.form.get('diastolic_bp')),
            'fasting_glucose': int(request.form.get('fasting_glucose')),
            'hemoglobin': float(request.form.get('hemoglobin')),
            'creatinine': float(request.form.get('creatinine')),
            'eGFR': float(request.form.get('eGFR')),
            'urine_protein': int(request.form.get('urine_protein')),
            'ast': int(request.form.get('AST')),
            'alt': int(request.form.get('ALT')),
            'rGTP': int(request.form.get('rGTP')), # 대문자 주의!
            'xray': int(request.form.get('xray')),
            'dental': int(request.form.get('dental_exam'))
        }
        
        sql = """
            INSERT INTO health_result (
                user_id, name, age, height, weight, BMI, waist, 
                vision_left, vision_right, hearing_left, hearing_right,
                systolic_bp, diastolic_bp, fasting_glucose, hemoglobin,
                creatinine, eGFR, urine_protein, AST, ALT, rGTP, xray, dental_exam
            ) VALUES (
                %(user_id)s, %(name)s, %(age)s, %(height)s, %(weight)s, %(bmi)s, %(waist)s,
                %(vision_left)s, %(vision_right)s, %(hearing_left)s, %(hearing_right)s,
                %(systolic_bp)s, %(diastolic_bp)s, %(fasting_glucose)s, %(hemoglobin)s,
                %(creatinine)s, %(eGFR)s, %(urine_protein)s, %(ast)s, %(alt)s, %(rGTP)s, %(xray)s, %(dental)s
            )
        """
        # 여기서 %(rGTP)s 처럼 data 딕셔너리의 키값과 정확히 일치해야 합니다.
        cursor.execute(sql, data)
        db.commit() 
        flash("성공적으로 등록되었습니다!")
        return redirect('/')
        
    except Exception as e:
        db.rollback() 
        print(f"!!! DB 저장 실제 오류 내용: {e}") # 중요: 터미널에 뜨는 이 내용을 봐야 합니다.
        flash(f"저장 실패: {e}")
        return redirect(url_for('health.create_health_record'))
        
    finally:
        cursor.close()
        db.close() # 필수! 연결 닫기
        
        
    
    
    
#----------------------------------------------------------------------- #
#--------------------------------허병철-------------------------- #
# ---------------------------------------------------------------------- #
@health_bp.route("/list/<int:id>", methods=["GET"])
def healthDetail(id):

    conn = getConnection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM health_result WHERE id = %s
    """, (id,))
    
    data = cursor.fetchone()
    
    cursor.close()
    conn.close()

    # 3. DB 저장 or 결과 반환
    return render_template("health/detail.html", data=data)