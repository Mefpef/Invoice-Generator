import hashlib

from flask import request, session, Blueprint, flash, redirect, url_for, render_template

from app.models.user import User

login_blueprint = Blueprint('login', __name__)


@login_blueprint.route('/')
@login_blueprint.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(login=username, password=password).first()

        if user:
            flash('Login successful', 'success')
            session['loggedin'] = True
            session['id'] = user['id']
            session['username'] = user['username']

            return redirect(url_for("admin_panel.admin_panel"))
        else:
            flash('Username or password incorrect !', 'warning')

    return render_template("base.html")
