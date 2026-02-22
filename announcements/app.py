from flask import Flask, request, render_template, Blueprint
from .forms import AnnouncementsForm
import sys
from scripts import announcements

announcements_bp = Blueprint("announcements", __name__, template_folder="templates")

@announcements_bp.route("/announcements", methods=['POST', 'GET'])
def announcements_handler():
    form = AnnouncementsForm(request.form)
    if request.method == "POST":
        try:
            result = announcements.main(request.form["line_code"])
            return render_template("announcements.html", form=form, result=result)
        except Exception as exc:
            return render_template("announcements.html", form=form, message=str(exc))
    # not a great approach
    return render_template("announcements.html", form=form)