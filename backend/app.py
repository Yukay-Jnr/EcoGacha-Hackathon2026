from flask import Flask
from flask_cors import CORS
from database import init_db
from services.ai_service import load_model
from routes.auth import auth_bp
from routes.scan import scan_bp
from routes.rewards import rewards_bp
from routes.users import users_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(scan_bp, url_prefix="/api/scan")
app.register_blueprint(rewards_bp, url_prefix="/api/rewards")
app.register_blueprint(users_bp, url_prefix="/api/users")

if __name__ == "__main__":
    init_db()
    load_model()          # loads rise_ai_model.pth — falls back to demo if not found
    app.run(debug=True, port=5000)
