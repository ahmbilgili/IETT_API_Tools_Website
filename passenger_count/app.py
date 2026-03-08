from flask import Flask, request, render_template, Blueprint
from .forms import PassengerCountForm
import sys
import threading
from scripts import passenger_count_day

passenger_count_bp = Blueprint("passenger_count", __name__, template_folder="templates")

@passenger_count_bp.route("/passenger_count", methods=['POST', 'GET'])
def passenger_count_day_handler():
    form = PassengerCountForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                result = passenger_count_day.main(request.form["date"])
                return render_template("passenger_count.html", form=form, result=result)
            except Exception as exc:
                return render_template("passenger_count.html", form=form, message=str(exc))
    # not a great approach
    return render_template("passenger_count.html", form=form)