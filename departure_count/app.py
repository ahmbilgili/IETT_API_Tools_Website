from flask import Flask, request, render_template, Blueprint
from .forms import DepartureCountForm
import sys
import threading
from scripts import departure_count_day

departure_count_bp = Blueprint("departure_count", __name__, template_folder="templates")

@departure_count_bp.route("/departure_count", methods=['POST', 'GET'])
def departure_count_day_handler():
    form = DepartureCountForm(request.form)
    if request.method == "POST":
        result = departure_count_day.main(request.form["date"])
        if type(result) not in [Exception, ValueError, TypeError]:
            return render_template("departure_count.html", form=form, result=result)
        return render_template("departure_count.html", form=form, message=result)
    # not a great approach
    return render_template("departure_count.html", form=form, result=[])