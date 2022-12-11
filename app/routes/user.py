from flask import request, session, Blueprint, flash, redirect, url_for, render_template
from flask_login import login_user, login_required, logout_user

from app.forms.invoice import InvoiceForm
from app.models.contractor import Contractor
from app.models.product import Product
from app.service.db import db
from app.models.user import User
from app.models.invoice import Invoice
from app.forms.register import RegisterForm
from app.forms.login import LoginForm

login_blueprint = Blueprint('login', __name__)
register_blueprint = Blueprint('register', __name__)
dashboard_blueprint = Blueprint('dashboard', __name__)
logout_blueprint = Blueprint('logout', __name__)

@login_blueprint.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user is not None and user.check_password(form.password.data):
            session['login'] = request.form['login']
            login_user(user)
            return redirect(url_for('dashboard.dashboard'))
        flash('Invalid login or password')
    return render_template("index.html", form=form)


@register_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(login=form.login.data, password=form.password.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login.login'))
    return render_template('register.html', form=form)


@dashboard_blueprint.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if 'login' in session:
        user = session['login']
        user = User.query.filter_by(login=user).first()
        print(user.id)
        invoice = Invoice.query.filter_by(user_id=user.id).first()
        contractor = Contractor.query.filter_by(user_contractor_id=user.id).first()

        return render_template('dashboard.html', invoice=invoice, contractor=contractor)


@logout_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login.login'))