import hashlib

from flask import request, session, Blueprint, flash, redirect, url_for, render_template

from app.models.user import User

login_blueprint = Blueprint('login', __name__)


@login_blueprint.route('/login', methods=["POST"])
def login():
    uname = request.form.get('username')
    passwd = request.form.get('password')
    session['username'] = uname
    user = User.query.filter_by(login=uname, password=passwd).first()
    if user:
        ulog = user.login
        return render_template('logged.html', ulogin=ulog)
    else:
        return render_template("index.html")
