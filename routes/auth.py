from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from dao.auth_dao import signInModule, signUpModule
from constants.auth import SIGNUP_SUCCESS, SIGNUP_DUPLICATE, SIGNUP_ERROR, SIGNUP_EMAIL, SIGNUP_PASSWORD


auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/signin", methods=["GET", "POST"])
def signIn():
    if request.method == "POST":
        user = signInModule(request)
        if(not user):
            flash("아이디 또는 비밀번호가 잘못되었습니다.", "warning")
            return redirect(url_for("auth.signIn"))
        
        session["user_id"] = user["id"]
        session["email"] = user["email"]
        session.permanent = True
        
        return redirect("/")
    
    # GET 요청이면 로그인 폼 보여주기
    return render_template("auth/signIn.html")

@auth_bp.route("/signup", methods=["GET", "POST"])
def signUp():
    if request.method == "POST":
        result = signUpModule(request)
        if result == SIGNUP_SUCCESS:
            flash("회원가입 완료!", "success")
            return redirect(url_for('auth.signIn'))

        elif result == SIGNUP_DUPLICATE:
            flash("이미 존재하는 이메일입니다.","warning")
            return redirect(url_for('auth.signUp'))
        
        elif result == SIGNUP_EMAIL:
            flash("이메일 형식에 맞게 입력하세요.","warning")
            return redirect(url_for('auth.signUp'))
        
        elif result == SIGNUP_PASSWORD:
            flash("비밀번호 형식에 맞게 입력하세요.","warning")
            return redirect(url_for('auth.signUp'))

        else:
            flash("회원가입에 실패했습니다.","danger")
            return redirect(url_for('auth.signUp'))
    
    # GET 요청이면 로그인 폼 보여주기
    return render_template("auth/signUp.html")

@auth_bp.route("/signOut")
def signOut():
    session.clear()  # 세션 전체 삭제 (가장 깔끔)
    return redirect(url_for("auth.signIn"))