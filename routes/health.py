from flask import Blueprint, render_template, redirect, url_for, session, request, flash, make_response
from db.connection import getConnection
from constants.health import HEALTH_SCHEMA, GRADE_TEXT, CATEGORY_TEXT, CATEGORY_REPORT
from dao.health_dao import calculate_age, calculate_exam_age, getNormalMinMax, get_category_summary, getUser, calculate_health_score
from dao.auth_decorators import checkSignIn
import pdfkit
from datetime import datetime
from urllib.parse import quote
import json

health_bp = Blueprint('health', __name__)

#----------------------------------------------------------------------- #
#--------------------------------김정범-------------------------- #
# ---------------------------------------------------------------------- #
@health_bp.route("/trend")
@checkSignIn
def healthTrend():
    user_id = session.get("user_id")
    conn = getConnection()
    try:
        with conn.cursor() as cursor:
            # 내 데이터만 날짜순(과거 -> 미래)으로 가져옵니다.
            sql = """
                SELECT * FROM health_result 
                WHERE user_id = %s 
                ORDER BY exam_date ASC
            """
            cursor.execute(sql, (user_id,))
            trend_data = cursor.fetchall()
            
            # 날짜가 없을 경우를 대비한 포맷팅 작업
            for row in trend_data:
                if row.get('exam_date'):
                    row['formatted_date'] = row['exam_date'].strftime('%Y-%m-%d')
                else:
                    row['formatted_date'] = "날짜 미입력"
                    
    finally:
        conn.close()

    print("#$##", trend_data)
    
    return render_template("health/trend.html", 
                           page_title="종합 건강 지표 추이", 
                           trend_data=trend_data)

@health_bp.route("/age")
@checkSignIn
def ageComparison():
    user_id = session.get("user_id")
    conn = getConnection()
    try:
        with conn.cursor() as cursor:
            sql_my = "SELECT * FROM health_result WHERE user_id = %s ORDER BY exam_date DESC"
            cursor.execute(sql_my, (user_id,))
            all_records = cursor.fetchall()
            
            if not all_records:
                return redirect(url_for('health.create_health_record'))
            
            latest_data = all_records[0]
            my_age = latest_data.get('age', 20)
            age_min = (my_age // 10) * 10
            
            sql_avg = """
                SELECT 
                    AVG(BMI) as avg_BMI,
                    AVG(systolic_bp) as avg_SBP,
                    AVG(diastolic_bp) as avg_DBP,
                    AVG(fasting_glucose) as avg_Glucose,
                    AVG(AST) as avg_AST,
                    AVG(ALT) as avg_ALT,
                    AVG(rGTP) as avg_rGTP
                FROM health_result 
                WHERE age >= %s AND age < %s
            """
            cursor.execute(sql_avg, (age_min, age_min + 10))
            group_avg = cursor.fetchone()

            for r in all_records:
                if r.get('exam_date'):
                    r['formatted_date'] = r['exam_date'].strftime('%Y-%m-%d')
                else:
                    r['formatted_date'] = "미상"
            
            # ★ [궁극의 마법 코드] JS가 뱉어내는 모든 에러(날짜, 소수점)를 무시하고 무조건 텍스트로 강제 변환!
            safe_records = json.dumps(all_records, default=str)
            safe_avg = json.dumps(group_avg, default=str) if group_avg else "{}"

    finally:
        conn.close()
        
    return render_template("health/age_comp.html", 
                           page_title="연령대별 지표 비교",
                           records=all_records,      # HTML 표 그리기용
                           group_avg=group_avg, 
                           age_group=age_min,
                           safe_records=safe_records, # JS 그래프 렌더링용 (에러 방지)
                           safe_avg=safe_avg,         # JS 그래프 렌더링용 (에러 방지)
                           schema=HEALTH_SCHEMA)


#----------------------------------------------------------------------- #
#--------------------------------정다희-------------------------- #
# ---------------------------------------------------------------------- #

@health_bp.route('/create', methods=['GET', 'POST']) # route에 메서드 명시 확인!
@checkSignIn
def create_health_record():
    if request.method == 'GET':
        return render_template('health/create.html')

    # 3. DB 저장
    db = getConnection()
    cursor = db.cursor()
    
    try:
        birth_date = request.form.get('birth_date')
        age = calculate_age(birth_date)

        data = {
            'user_id' : session.get("user_id"),
            'name': request.form.get('name'),
            'exam_date': request.form.get('exam_date'),
            'birth_date' : birth_date,
            'age' : age,
            'gender': request.form.get('gender'),
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
        
        # risk 룰 조회
        cursor.execute("SELECT * FROM health_risk")
        risk_rules = cursor.fetchall()

        # 점수 계산
        _, score, grade = calculate_health_score(data, risk_rules)

        # data에 추가
        data["score"] = score
        data["grade"] = grade

        sql = """
            INSERT INTO health_result (
                user_id, name, gender, age, birth_date, exam_date, height, weight, BMI, waist, 
                vision_left, vision_right, hearing_left, hearing_right,
                systolic_bp, diastolic_bp, fasting_glucose, hemoglobin,
                creatinine, eGFR, urine_protein, AST, ALT, rGTP, xray, dental_exam,
                score, grade
            ) VALUES (
                %(user_id)s, %(name)s, %(gender)s, %(age)s, %(birth_date)s, %(exam_date)s, %(height)s, %(weight)s, %(bmi)s, %(waist)s,
                %(vision_left)s, %(vision_right)s, %(hearing_left)s, %(hearing_right)s,
                %(systolic_bp)s, %(diastolic_bp)s, %(fasting_glucose)s, %(hemoglobin)s,
                %(creatinine)s, %(eGFR)s, %(urine_protein)s, %(ast)s, %(alt)s, %(rGTP)s, %(xray)s, %(dental)s,
                %(score)s, %(grade)s
            )
        """
        # 여기서 %(rGTP)s 처럼 data 딕셔너리의 키값과 정확히 일치해야 합니다.
        cursor.execute(sql, data)
        db.commit() 
        flash("성공적으로 등록되었습니다!", "success")
        return redirect(url_for('health.getHealthList'))
        
    except Exception as e:
        db.rollback() 
        print(f"!!! DB 저장 실제 오류 내용: {e}") # 중요: 터미널에 뜨는 이 내용을 봐야 합니다.
        flash(f"등록 실패", "danger")
        return redirect(url_for('health.create_health_record'))
        
    finally:
        cursor.close()
        db.close() # 필수! 연결 닫기
    
#----------------------------------------------------------------------- #
#--------------------------------허병철-------------------------- #
# ---------------------------------------------------------------------- #

@health_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@checkSignIn
def edit_health_record(id):
    db = getConnection()
    cursor = db.cursor()

    try:
        # =========================
        # GET (조회)
        # =========================
        if request.method == 'GET':
            cursor.execute("SELECT * FROM health_result WHERE id = %s", (id,))
            data = cursor.fetchone()

            return render_template(
                'health/edit.html',
                data=data,
                mode="edit"
            )

        # =========================
        # POST (수정)
        # =========================
        birth_date = request.form.get('birth_date')
        age = calculate_age(birth_date)

        data = {
            'id': id,
            'user_id': session.get("user_id"),

            'name': request.form.get('name'),
            'exam_date': request.form.get('exam_date'),
            'birth_date': birth_date,
            'age': age,
            'gender': request.form.get('gender'),

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

        # =========================
        # risk 재계산
        # =========================
        cursor.execute("SELECT * FROM health_risk")
        risk_rules = cursor.fetchall()

        _, score, grade = calculate_health_score(data, risk_rules)

        data["score"] = score
        data["grade"] = grade

        # =========================
        # UPDATE SQL
        # =========================
        sql = """
            UPDATE health_result SET
                user_id=%(user_id)s,
                name=%(name)s,
                gender=%(gender)s,
                age=%(age)s,
                birth_date=%(birth_date)s,
                exam_date=%(exam_date)s,

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
                dental_exam=%(dental)s,

                score=%(score)s,
                grade=%(grade)s
            WHERE id=%(id)s
        """

        cursor.execute(sql, data)
        db.commit()

        flash("내용을 수정했습니다.", "success")
        return redirect(url_for('health.healthDetail', id=id))

    except Exception as e:
        db.rollback()
        print(f"!!! UPDATE ERROR: {e}")
        flash(f"수정 실패", "danger")
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
        flash("삭제가 완료되었습니다", "success")

    except Exception as e:
        db.rollback()
        flash(f"삭제 실패", "danger")

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

    if not data:
        cursor.close()
        conn.close()
        return render_template(
            "health/detail.html",
            data=None,
            schema=HEALTH_SCHEMA,
            result_labels={},
        )

    cursor.execute("""
        SELECT * FROM health_risk
    """)
    risk_rules = cursor.fetchall()
    
    cursor.close()
    conn.close()

    (result_labels, score, grade) = calculate_health_score(data, risk_rules)
    category_summary = get_category_summary(result_labels)

    normal_data = getNormalMinMax()

    ui_context = {
        "schema" :HEALTH_SCHEMA,
        "grade" : GRADE_TEXT,
        "category" : {
            "text": CATEGORY_TEXT,
            "report": CATEGORY_REPORT
        }
    }

    # 3. 결과 반환
    return render_template("health/detail.html", data=data, ui_context=ui_context, result_labels=result_labels, category_summary=category_summary, normal_data=normal_data)

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
    name = request.args.get("name")  # name 검색 파라미터

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
        base_query += " AND YEAR(exam_date) = %s"
        params.append(year)

    # 🔥 name 검색 필터
    if name:
        base_query += " AND name LIKE %s"
        params.append(f"%{name}%")

    # 정렬
    order_query = " ORDER BY exam_date DESC"
    if sort == "asc":
        order_query = " ORDER BY exam_date ASC"

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
        sort=sort,
        name=name,  # name 파라미터를 템플릿으로 전달
        schema=HEALTH_SCHEMA, 
    )