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
        if form.validate_on_submit():
            try:
                result = departure_count_day.main(request.form["date"])
                return render_template("departure_count.html", form=form, result=result)
            except Exception as exc:
                return render_template("departure_count.html", form=form, message=str(exc))
    # not a great approach
    return render_template("departure_count.html", form=form)