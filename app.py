from flask import Flask, request, render_template, Blueprint, Response
from flask_wtf import CSRFProtect
import os
from announcements.app import announcements_bp
from archive.app import archive_bp
from passenger_count.app import passenger_count_bp
from departure_hours.app import departure_hours_bp
from line_service.app import line_service_bp
from feedback.app import feedback_bp
from captcha.image import ImageCaptcha
import random
import redis
import time

os.environ["IN_PROD"] = "True"
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
app.register_blueprint(feedback_bp)

csrf = CSRFProtect(app=app)
csrf.init_app(app)

# DB Credentials
REDIS_DB_IP = os.getenv("REDIS_DB_IP")
REDIS_DB_PORT = os.getenv("REDIS_DB_PORT")
REDIS_DB_USER = os.getenv("REDIS_DB_USER")
REDIS_DB_PASSWORD = os.getenv("REDIS_DB_PASSWORD")

# Rate limiter config
RATE_LIMIT = 30
RATE_LIMIT_WINDOW = 60

redis_client = redis.Redis(
    host=REDIS_DB_IP,
    port=int(REDIS_DB_PORT),
    decode_responses=True,
    username=REDIS_DB_USER,
    password=REDIS_DB_PASSWORD
)

@app.before_request
def vibe_check():
    key = request.remote_addr
    curr_time = int(time.time())
    
    # pipe that can queue multiple commands for later execution
    pipe = redis_client.pipeline()

    pipe.zadd(key, {f"now: {curr_time}": curr_time})

    if redis_client.zcard(key) == 0:
        # Setting exp date on key
        pipe.expire(key, RATE_LIMIT_WINDOW)

    # Removing records that are older than (current_time - rate_limit_window)
    # pipe.zremrangebyrank(key, min=0, max=curr_time - RATE_LIMIT_WINDOW)

    # Get the current # of requests
    pipe.zcard(key)

    result = pipe.execute()
    
    if len(result) == 3:
        num_of_req = result[2]
    else:
        num_of_req = result[1]

    if num_of_req >= RATE_LIMIT:
        return Response("You've sent too many requests in a short period of time, please wait until cooldown period ends", status=429)
    
@app.route("/", methods=['GET'])
def base_handler():
    return render_template("base.html")

'''
def run_app():
    app.run(host="127.0.0.1", port=50000, debug=True)

if __name__ == "__main__":
    run_app()
'''