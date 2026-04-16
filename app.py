from flask import Flask
from routes.auth_routes import auth_bp

app = Flask(__name__)

# Blueprint 등록
app.register_blueprint(auth_bp, url_prefix="/auth")

if __name__ == "__main__":
    app.run(debug=True)