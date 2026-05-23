from flask import Flask, request, render_template, Blueprint, session, g
import sys
import threading

version_bp = Blueprint("version", __name__, template_folder="templates")

@version_bp.route("/version", methods=['GET'])
def version_handler():
    return render_template("version.html", version_info=g.version_info)