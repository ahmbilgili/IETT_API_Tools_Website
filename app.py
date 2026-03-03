from flask import Flask, request, render_template, Blueprint
from flask_wtf import CSRFProtect
from dotenv import load_dotenv
import os
from announcements.app import announcements_bp
from archive.app import archive_bp
from departure_count.app import departure_count_bp
from departure_hours.app import departure_hours_bp
from line_service.app import line_service_bp
from config import DEV_ENV

if DEV_ENV:
    # Loads config file from parent dir
    load_dotenv(dotenv_path="../config.env")
else:
    # Loads config file from current dir (app)
    load_dotenv(dotenv_path="./config.env")

app = Flask(__name__)
#app.config.from_pyfile("config.py")
app.config["SECRET_KEY"] = os.getenv("WTF_CSRF_SECRET_KEY")
app.register_blueprint(announcements_bp)
app.register_blueprint(archive_bp)
app.register_blueprint(departure_count_bp)
app.register_blueprint(departure_hours_bp)
app.register_blueprint(line_service_bp)

csrf = CSRFProtect(app=app)
csrf.init_app(app)

@app.route("/", methods=['GET'])
def base_handler():
    return render_template("base.html")

def run_app():
    app.run(host="127.0.0.1", port=50000, debug=True)

if __name__ == "__main__":
    run_app()
