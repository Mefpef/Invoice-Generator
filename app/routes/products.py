from flask import request, Blueprint, render_template, flash, redirect, url_for, session
from flask_login import login_required
from app.forms.product import ProductForm
from app.models.product import Product
from app.models.user import User
from app.service.db import db

add_product_blueprint = Blueprint('add_product', __name__)

@add_product_blueprint.route('/add_product', methods=["POST", "GET"])
@login_required
def add_product():
    form = ProductForm()
    if 'login' in session:
        user = session['login']
        user = User.query.filter_by(login=user).first()

        if form.validate_on_submit():
            new_product = Product(name=form.name.data, description=form.description.data, pkwiu=form.pkwiu.data, cn=form.cn.data,
                                  price=form.price.data, user_product_id=user.id)

            db.session.add(new_product)
            db.session.commit()

            return redirect(url_for('dashboard.dashboard'))