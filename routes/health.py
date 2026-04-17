from flask import Blueprint, render_template, redirect, url_for, session, request, flash, make_response
from db.connection import getConnection
import pymysql
from constants.health import BASE_SCORE, HEALTH_SCHEMA
from dao.health_dao import getGrade, getUser
from dao.auth_decorators import checkSignIn
import pdfkit
from datetime import datetime
from urllib.parse import quote

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

# 건강검진 결과(by id) 업데이트
@health_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@checkSignIn
def edit_health_record(id):
    db = getConnection()
    cursor = db.cursor()

    if request.method == 'GET':
        cursor.execute("SELECT * FROM health_result WHERE id = %s", (id,))
        data = cursor.fetchone()
        cursor.close()
        db.close()
        return render_template('health/check.html', data=data, mode="edit")

    try:
        data = {
            'id': id,
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
            'rGTP': int(request.form.get('rGTP')),
            'xray': int(request.form.get('xray')),
            'dental': int(request.form.get('dental_exam'))
        }

        sql = """
            UPDATE health_result SET
                name=%(name)s,
                age=%(age)s,
                height=%(height)s,
                weight=%(weight)s,
                BMI=%(bmi)s,
                waist=%(waist)s,
                vision_left=%(vision_left)s,
                vision_right=%(vision_right)s,
                hearing_left=%(hearing_left)s,
                hearing_right=%(hearing_right)s,
                systolic_bp=%(systolic_bp)s,
                diastolic_bp=%(diastolic_bp)s,
                fasting_glucose=%(fasting_glucose)s,
                hemoglobin=%(hemoglobin)s,
                creatinine=%(creatinine)s,
                eGFR=%(eGFR)s,
                urine_protein=%(urine_protein)s,
                AST=%(ast)s,
                ALT=%(alt)s,
                rGTP=%(rGTP)s,
                xray=%(xray)s,
                dental_exam=%(dental)s
            WHERE id=%(id)s
        """

        cursor.execute(sql, data)
        db.commit()

        flash("수정 완료!")
        return redirect(url_for('health.health_detail', id=id))

    except Exception as e:
        db.rollback()
        flash(f"수정 실패: {e}")
        return redirect(url_for('health.edit_health_record', id=id))

    finally:
        cursor.close()
        db.close()

# 건강검진 결과(by id) 삭제
@health_bp.route('/delete/<int:id>', methods=['POST'])
@checkSignIn
def delete_health_record(id):

    db = getConnection()
    cursor = db.cursor()

    try:
        cursor.execute("""
            DELETE FROM health_result
            WHERE id = %s
        """, (id,))

        db.commit()
        flash("삭제 완료!")

    except Exception as e:
        db.rollback()
        flash(f"삭제 실패: {e}")

    finally:
        cursor.close()
        db.close()

    return redirect(url_for('health.getHealthList'))

# 건강검진 결과 하나(by id) 조회
@health_bp.route("/list/<int:id>", methods=["GET"])
@checkSignIn
def healthDetail(id):

    conn = getConnection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM health_result WHERE id = %s
    """,
    (id,)
    )
    data = cursor.fetchone()

    cursor.execute("""
        SELECT * FROM health_risk
    """)
    risk_rules = cursor.fetchall()
    
    cursor.close()
    conn.close()

    result_labels = {}
    score = BASE_SCORE

    for rule in risk_rules:

        item = rule["item_name"]

        # 1. 그룹 확장
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

        # 2. 각 target 개별 검사
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
                    "color_hex": color
                }
                score -= risk
        
    grade = getGrade(score)

    # 3. 결과 반환
    return render_template("health/detail.html", data=data, schema=HEALTH_SCHEMA, result_labels=result_labels, score=score, grade=grade)

# 건강검진 결과 리스트(by user_id)
@health_bp.route("/list", methods=["GET"])
@checkSignIn
def getHealthList():
    user_id = session.get("user_id")

    # query params
    page = int(request.args.get("page", 1))
    per_page = 10

    year = request.args.get("year")  # ex) 2026
    sort = request.args.get("sort", "desc")  # asc | desc

    offset = (page - 1) * per_page

    conn = getConnection()
    cur = conn.cursor()

    # 기본 쿼리
    base_query = """
        FROM health_result
        WHERE user_id = %s
    """

    params = [user_id]

    # 🔥 연도 필터
    if year:
        base_query += " AND YEAR(created_at) = %s"
        params.append(year)

    # 정렬
    order_query = " ORDER BY created_at DESC"
    if sort == "asc":
        order_query = " ORDER BY created_at ASC"

    # 데이터 조회
    data_query = f"""
        SELECT *
        {base_query}
        {order_query}
        LIMIT %s OFFSET %s
    """

    cur.execute(data_query, params + [per_page, offset])
    rows = cur.fetchall()

    # 전체 개수 (페이지네이션용)
    count_query = f"""
        SELECT COUNT(*)
        {base_query}
    """

    cur.execute(count_query, params)

    total_count = cur.fetchone()["COUNT(*)"]
    total_pages = (total_count + per_page - 1) // per_page

    return render_template(
        "health/list.html",
        rows=rows,
        page=page,
        total_pages=total_pages,
        year=year,
        sort=sort
    )

# PDF 다운 - 작동에러있음 수정 필요
@health_bp.route("/download/pdf/<int:id>")
@checkSignIn
def download_pdf(id):

    # 1. HTML 생성 (해당 검사 id 기준)
    html = healthDetail(id)

    config = pdfkit.configuration(
        wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    )

    options = {
        'enable-local-file-access': None
    }

    # 2. PDF 생성
    pdf = pdfkit.from_string(html, False, configuration=config, options=options)

    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"

    # 3. 사용자 정보 가져오기
    user_id = session.get("user_id")
    user = getUser(user_id)

    # 4. 파일명 생성 (20260302_허병철_건강검진결과.pdf)
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"{date_str}_{user['name']}_건강검진결과.pdf"

    # 5. 한글 안전 처리
    encoded_filename = quote(filename)

    response.headers["Content-Disposition"] = (
        f"attachment; filename={encoded_filename}"
    )

    return response