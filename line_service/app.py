from flask import Flask, request, render_template, Blueprint, session
from .forms import LineServiceForm
import sys
import threading
from scripts import line_service
from scripts.utils.functions import generate_captcha

line_service_bp = Blueprint("line_service", __name__, template_folder="templates")

@line_service_bp.route("/line_service", methods=['POST', 'GET'])
def line_service_handler():
    form = LineServiceForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                if request.form["captcha"] != session["captcha_code"]:
                    raise Exception("Incorrect captcha!")
                # generate new captcha
                captcha_code, captcha_data = generate_captcha()
                session["captcha_code"] = captcha_code
                result = line_service.main(request.form["line_code"])
                return render_template("line_service.html", form=form, result=result, captcha=captcha_data)
            except Exception as exc:
                captcha_code, captcha_data = generate_captcha()
                session["captcha_code"] = captcha_code
                return render_template("line_service.html", form=form, message=str(exc), captcha=captcha_data)
        else:
            captcha_code, captcha_data = generate_captcha()
            session["captcha_code"] = captcha_code
            return render_template("line_service.html", form=form, message=form.errors.values(), captcha=captcha_data)
    captcha_code, captcha_data = generate_captcha()
    session["captcha_code"] = captcha_code
    return render_template("line_service.html", form=form, captcha=captcha_data)