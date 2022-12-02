from flask import request, session, Blueprint, flash, redirect, url_for, render_template
from flask_login import login_user

from app.models.user import User

login_blueprint = Blueprint('login', __name__)
register_blueprint = Blueprint('register', __name__)


@login_blueprint.route('/login', methods=["POST"])
def login():
    uname = request.form.get('username')
    passwd = request.form.get('password')
    session['username'] = uname
    user = User.query.filter_by(login=uname, password=passwd).first()
    if user:
        login_user(user)
        ulog = user.login
        return render_template('dashboard.html', ulogin=ulog)
    else:
        return render_template("index.html")


@register_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    pass