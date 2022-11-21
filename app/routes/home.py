from flask import Blueprint, redirect, url_for

home_blueprint = Blueprint('home_blueprint', __name__)


@home_blueprint.route("/")
def home():
    return redirect(url_for("index.index"))
