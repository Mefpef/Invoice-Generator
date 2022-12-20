from flask import Blueprint, render_template

from app.forms.login import LoginForm

index_blueprint = Blueprint('index_blueprint', __name__)


@index_blueprint.route("/")
def home():
    form = LoginForm()
    return render_template('index.html', form=form)
