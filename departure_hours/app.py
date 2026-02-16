from flask import Flask, request, render_template, Blueprint
from .forms import DepartureHoursForm
import sys
import threading
from scripts import scheduled_departure_hours

departure_hours_bp = Blueprint("departure_hours", __name__, template_folder="templates")

@departure_hours_bp.route("/departure_hours", methods=['POST', 'GET'])
def departure_hours_handler():
    form = DepartureHoursForm(request.form)
    if request.method == "POST":
        result = scheduled_departure_hours.main(request.form["line_code"], request.form["direction"], request.form["day"])
        return render_template("departure_hours.html", form=form, result=result)
    # not a great approach
    return render_template("departure_hours.html", form=form, result=[])
