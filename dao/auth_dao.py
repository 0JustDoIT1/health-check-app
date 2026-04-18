from argon2 import PasswordHasher
from db.connection import getConnection
from constants.auth import SIGNUP_SUCCESS, SIGNUP_DUPLICATE, SIGNUP_ERROR, SIGNUP_EMAIL, SIGNUP_PASSWORD
import re
from constants.regex import NAME_REGEX, EMAIL_REGEX, PASSWORD_REGEX

ph = PasswordHasher()

# 로그인 모듈
def signInModule(request):
    # 폼 데이터 가져오기
    email = request.form.get("email")
    password = request.form.get("password")
    
    conn = getConnection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT * FROM user WHERE email=%s
        """,
        (email,)
    )
    user = cur.fetchone()
    
    cur.close()
    conn.close()

    if not user:
        return None
    
    try:
        ph.verify(user["password"], password)
        return user
    except Exception as e:
        return None

# 이메일 중복 확인
def checkExistUser(cur, email):
    cur.execute("""
        SELECT * FROM user WHERE email=%s 
        """,
        (email, )
    )
    return cur.fetchone()

# 회원가입 모듈
def signUpModule(request):
    name = request.form.get("name")
    email = request.form.get("email")
    birth_date = request.form.get("birth_date")
    gender = request.form.get("gender")
    password = request.form.get("password")
    repassword = request.form.get("re_password")
    
    if not name or not email or not password or not birth_date or not gender:
        return SIGNUP_ERROR  # 필수 입력값이 하나라도 비어 있으면 오류
    
    if gender not in ['male', 'female']:
        return SIGNUP_ERROR
    
    if not re.match(NAME_REGEX, name):
        return SIGNUP_ERROR
    
    if not re.match(EMAIL_REGEX, email):
        return SIGNUP_EMAIL
    
    if not re.match(PASSWORD_REGEX, password):
        return SIGNUP_PASSWORD
    
    if password != repassword:
        return SIGNUP_PASSWORD

    conn = getConnection()
    cur = conn.cursor()

    try:
        existUser = checkExistUser(cur, email)
        if existUser:
            return SIGNUP_DUPLICATE

        hashPassword = ph.hash(password)

        # 성별과 생년월일을 함께 INSERT 쿼리에 추가
        cur.execute("""
            INSERT INTO user (name, email, password, gender, birth_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, email, hashPassword, gender, birth_date))
        
        conn.commit()

        return SIGNUP_SUCCESS

    except Exception as e:
        conn.rollback()
        return SIGNUP_ERROR

    finally:
        cur.close()
        conn.close()