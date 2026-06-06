import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from database import init_db
from services.ai_service import load_model
from routes.auth import auth_bp
from routes.scan import scan_bp
from routes.rewards import rewards_bp
from routes.users import users_bp

# Tell Flask where the frontend folder is
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
CORS(app)

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(scan_bp, url_prefix="/api/scan")
app.register_blueprint(rewards_bp, url_prefix="/api/rewards")
app.register_blueprint(users_bp, url_prefix="/api/users")

# Serve the frontend
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    init_db()
    load_model()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))