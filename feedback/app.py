from flask import Flask, request, render_template, Blueprint, session
from .forms import FeedbackForm
import sys
import threading
from scripts import passenger_count_day
from scripts.utils.wrapper_functions import *
from scripts.utils.functions import generate_captcha
from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey, Date
import datetime

feedback_bp = Blueprint("feedback", __name__, template_folder="templates")

metadata = MetaData()

feedback_table = Table(
    "feedback",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String),
    Column("feedback", String),
    Column("date", Date)
)

@feedback_bp.route("/feedback", methods=['POST', 'GET'])
def feedback_handler():
    form = FeedbackForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                if request.form["captcha"] != session["captcha_code"]:
                    raise Exception("Incorrect captcha!")
                email = form.email.data
                feedback = form.feedback.data
                current_date = datetime.datetime.today().strftime("%Y-%m-%d")
                data_to_insert = {"email": email, "feedback": feedback, "date": current_date}
                result = insert_to_db("feedback_user", os.getenv("MARIADB_FEEDBACK_USER_PASSWORD"), feedback_table, data_to_insert)
                if result:
                    captcha_code, captcha_data = generate_captcha()
                    session["captcha_code"] = captcha_code
                    return render_template("feedback.html", form=form, captcha=captcha_data, message="Thank you for your feedback, it will be considered thoroughly")
                else:
                    raise Exception("Error while sending form data to server")
            except Exception as exc:
                captcha_code, captcha_data = generate_captcha()
                session["captcha_code"] = captcha_code
                return render_template("feedback.html", form=form, error=str(exc), captcha=captcha_data)
        else:
            captcha_code, captcha_data = generate_captcha()
            session["captcha_code"] = captcha_code
            return render_template("feedback.html", form=form, captcha=captcha_data, error="Couldn't validate your form")
    captcha_code, captcha_data = generate_captcha()
    session["captcha_code"] = captcha_code
    return render_template("feedback.html", captcha=captcha_data, form=form)