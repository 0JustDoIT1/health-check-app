from flask import Flask
from routes.user_routes import user_bp

app = Flask(__name__)

# Blueprint 등록
app.register_blueprint(user_bp)

if __name__ == "__main__":
    app.run(debug=True)