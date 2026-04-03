from flask import Flask, request, render_template, Blueprint, session
from .forms import ArchiveForm
import sys
import threading
from scripts import archive
from scripts.utils.functions import generate_captcha

archive_bp = Blueprint("archive", __name__, template_folder="templates")

@archive_bp.route("/archive", methods=['POST', 'GET'])
def archive_handler():
    form = ArchiveForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                if request.form["captcha"] != session["captcha_code"]:
                    raise Exception("Incorrect captcha!")
                captcha_code, captcha_data = generate_captcha()
                session["captcha_code"] = captcha_code
                result = archive.main(request.form["date"], request.form["line_code"])
                return render_template("archive.html", form=form, result=result, captcha=captcha_data)
            except Exception as exc:
                captcha_code, captcha_data = generate_captcha()
                session["captcha_code"] = captcha_code
                return render_template("archive.html", form=form, message=str(exc), captcha=captcha_data)
        else:
            captcha_code, captcha_data = generate_captcha()
            session["captcha_code"] = captcha_code
            return render_template("archive.html", form=form, message=form.errors.values(), captcha=captcha_data)
    captcha_code, captcha_data = generate_captcha()
    session["captcha_code"] = captcha_code
    return render_template("archive.html", form=form, captcha=captcha_data)