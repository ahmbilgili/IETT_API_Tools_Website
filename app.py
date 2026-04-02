from flask import Flask, request, render_template, Blueprint, Response
from flask_wtf import CSRFProtect
import os
from announcements.app import announcements_bp
from archive.app import archive_bp
from passenger_count.app import passenger_count_bp
from departure_hours.app import departure_hours_bp
from line_service.app import line_service_bp
from captcha.image import ImageCaptcha
import random

random.seed(10)


app = Flask(__name__)
image = ImageCaptcha()
app.config.from_pyfile("config.py")
app.config["SECRET_KEY"] = os.getenv("WTF_CSRF_SECRET_KEY")
app.config["RECAPTCHA_PUBLIC_KEY"] = os.getenv("RECAPTCHA_PUBLIC_KEY")
app.config["RECAPTCHA_PRIVATE_KEY"] = os.getenv("RECAPTCHA_PRIVATE_KEY")
app.register_blueprint(announcements_bp)
app.register_blueprint(archive_bp)
app.register_blueprint(passenger_count_bp)
app.register_blueprint(departure_hours_bp)
app.register_blueprint(line_service_bp)

csrf = CSRFProtect(app=app)
csrf.init_app(app)

print(os.getenv("SSH_USERNAME"))
@app.route("/", methods=['GET'])
def base_handler():
    return render_template("base.html")

@app.route("/captcha")
def captcha_view():
    # add your own logic to generate the code
    ascii_codes = range(97, 122)
    code = ""
    for i in range(4):
        character_type = random.randint(0, 1)
        if character_type == 0:
            code += chr(random.randint(97, 122))
        else:
            code += chr(random.randint(48, 57))
    data = image.generate(code)
    return Response(data, mimetype="image/png")

def run_app():
    app.run(host="127.0.0.1", port=50000, debug=True)

if __name__ == "__main__":
    run_app()