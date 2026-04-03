from flask import Flask, request, render_template, Blueprint, session
from .forms import PassengerCountForm
import sys
import threading
from scripts import passenger_count_day
from scripts.utils.functions import generate_captcha

passenger_count_bp = Blueprint("passenger_count", __name__, template_folder="templates")

@passenger_count_bp.route("/passenger_count", methods=['POST', 'GET'])
def passenger_count_day_handler():
    form = PassengerCountForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                if request.form["captcha"] != session["captcha_code"]:
                    raise Exception("Incorrect captcha!")
                # generate new captcha
                captcha_code, captcha_data = generate_captcha()
                session["captcha_code"] = captcha_code
                result = passenger_count_day.main(request.form["date"])
                return render_template("passenger_count.html", form=form, result=result, captcha=captcha_data)
            except Exception as exc:
                captcha_code, captcha_data = generate_captcha()
                session["captcha_code"] = captcha_code
                return render_template("passenger_count.html", form=form, message=str(exc), captcha=captcha_data)    
        else:
            captcha_code, captcha_data = generate_captcha()
            session["captcha_code"] = captcha_code
            return render_template("passenger_count.html", form=form, message=form.errors.values(), captcha=captcha_data)        
    captcha_code, captcha_data = generate_captcha()
    session["captcha_code"] = captcha_code
    return render_template("passenger_count.html", form=form, captcha=captcha_data)