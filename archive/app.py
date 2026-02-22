from flask import Flask, request, render_template, Blueprint
from .forms import ArchiveForm
import sys
import threading
from scripts import archive

archive_bp = Blueprint("archive", __name__, template_folder="templates")

@archive_bp.route("/archive", methods=['POST', 'GET'])
def archive_handler():
    form = ArchiveForm(request.form)
    if request.method == "POST":
        try:
            result = archive.main(request.form["date"], request.form["line_code"])
            return render_template("archive.html", form=form, result=result)
        except Exception as exc:
            return render_template("archive.html", form=form, message=str(exc))
    # not a great approach
    return render_template("archive.html", form=form)