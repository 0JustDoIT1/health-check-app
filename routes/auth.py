from flask import Blueprint, render_template, request, redirect, url_for, flash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        # 폼 데이터 가져오기
        username = request.form.get("username")
        password = request.form.get("password")
        
        # 사용자 검증 (예시)
        if username == "admin" and password == "1234":
            # 로그인 성공 처리 (세션 저장 등)
            return redirect(url_for("main.index"))  # 로그인 후 이동
        else:
            flash("아이디 또는 비밀번호가 잘못되었습니다.")
            return redirect(url_for("auth.signin"))
    
    # GET 요청이면 로그인 폼 보여주기
    return render_template("auth/signin.html")
