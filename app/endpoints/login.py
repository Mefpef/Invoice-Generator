import hashlib

from flask import request, session, Blueprint, flash, redirect, url_for, render_template

from app.models import Admins

login_blueprint = Blueprint('login', __name__)


@login_blueprint.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        session.permanent = True

        encryptor = hashlib.sha512()
        username = request.form["username"]
        password = request.form["password"]
        encryptor.update(str.encode(password))
        password_hash = encryptor.hexdigest()

        found_user = Admins.query.filter_by(user=username, password=password_hash).first()

        if found_user:
            flash('Login successful', 'success')
            session['username'] = found_user.user

            return redirect(url_for("admin_panel.admin_panel"))
        else:
            flash('Username or password incorrect !', 'warning')

    return render_template("login.html")
