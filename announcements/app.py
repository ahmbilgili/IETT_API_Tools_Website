from flask import Flask, request, render_template, Blueprint, session
from .forms import AnnouncementsForm
import sys
from scripts import announcements
from scripts.utils.functions import generate_captcha
import os

announcements_bp = Blueprint("announcements", __name__, template_folder="templates")

@announcements_bp.route("/announcements", methods=['POST', 'GET'])
def announcements_handler():
    form = AnnouncementsForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                if request.form["captcha"] != session["captcha_code"]:
                    raise Exception("Incorrect captcha!")
                # generate new captcha
                captcha_code, captcha_data = generate_captcha()
                session["captcha_code"] = captcha_code
                result = announcements.main(request.form["line_code"])
                return render_template("announcements.html", form=form, result=result, captcha=captcha_data)
            except Exception as exc:
                captcha_code, captcha_data = generate_captcha()
                session["captcha_code"] = captcha_code
                return render_template("announcements.html", form=form, message=str(exc), captcha=captcha_data)
        else:
            captcha_code, captcha_data = generate_captcha()
            session["captcha_code"] = captcha_code
            return render_template("announcements.html", form=form, message=form.errors.values(), captcha=captcha_data)
    captcha_code, captcha_data = generate_captcha()
    session["captcha_code"] = captcha_code
    return render_template("announcements.html", form=form, captcha=captcha_data)