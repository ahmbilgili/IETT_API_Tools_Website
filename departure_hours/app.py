from flask import Flask, request, render_template, Blueprint, session
from .forms import DepartureHoursForm
import sys
import threading
from scripts import scheduled_departure_hours
from scripts.utils.functions import generate_captcha

departure_hours_bp = Blueprint("departure_hours", __name__, template_folder="templates")

@departure_hours_bp.route("/departure_hours", methods=['POST', 'GET'])
def departure_hours_handler():
    form = DepartureHoursForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            if "direction" in request.form:
                try:
                    if request.form["captcha"] != session["captcha_code"]:
                        raise Exception("Incorrect captcha!")
                    # generate new captcha
                    result = scheduled_departure_hours.main(request.form["line_code"], request.form["day"], request.form["direction"])
                    return render_template("departure_hours.html", form=form, status="initial", result=result)
                except Exception as exc:
                    return render_template("departure_hours.html", form=form, status="initial", message=str(exc))
            else:
                # Line code and day is submitted. Check if an exception is raised.
                # If so, return the initial form. Otherwise, return the updated form by adding direction field.
                try:
                    # generate captcha, we're in the step of choosing direction.
                    captcha_code, captcha_data = generate_captcha()
                    session["captcha_code"] = captcha_code
                    line_info = scheduled_departure_hours.main(request.form["line_code"], request.form["day"], querying_for_line=True)
                    return render_template("departure_hours.html", form=form, status="final", line_info=line_info, captcha=captcha_data)
                except Exception as exc:
                    # An exception was returned as a result, so don't enable the direction field.
                    return render_template("departure_hours.html", form=form, status="initial", message=str(exc))
        else:
            captcha_code, captcha_data = generate_captcha()
            session["captcha_code"] = captcha_code
            return render_template("departure_hours.html", form=form, message=form.errors.values(), captcha=captcha_data)
    # GET request, show line code and day field only. Don't show direction yet.
    return render_template("departure_hours.html", form=form, status="initial")
