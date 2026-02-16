from flask import Flask, request, render_template, Blueprint
from .forms import AnnouncmentsForm
import sys
from scripts import announcments

announcments_bp = Blueprint("announcments", __name__, template_folder="templates")

@announcments_bp.route("/announcments", methods=['POST', 'GET'])
def announcments_handler():
    form = AnnouncmentsForm(request.form)
    if request.method == "POST":
        result = announcments.main(request.form["line_code"])
        return render_template("announcments.html", form=form, result=result)
    # not a great approach
    return render_template("announcments.html", form=form, result=[])