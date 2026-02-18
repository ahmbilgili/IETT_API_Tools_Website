from flask import Flask, request, render_template, Blueprint
from .forms import LineServiceForm
import sys
import threading
from scripts import line_service

line_service_bp = Blueprint("line_service", __name__, template_folder="templates")

@line_service_bp.route("/line_service", methods=['POST', 'GET'])
def line_service_handler():
    form = LineServiceForm(request.form)
    if request.method == "POST":
        result = line_service.main(request.form["line_code"])
        if type(result) not in [Exception, ValueError, TypeError]:
            return render_template("line_service.html", form=form, result=result)
        return render_template("line_service.html", form=form, message=result)
    # not a great approach
    return render_template("line_service.html", form=form, result=[])