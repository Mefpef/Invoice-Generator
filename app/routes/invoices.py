from datetime import date

from flask import request, Blueprint, render_template, flash, redirect, url_for, session
from flask_login import login_required

from app.forms.invoice import InvoiceForm
from app.models.contractor import Contractor
from app.models.invoice import Invoice
from app.models.product import Product
from app.models.user import User
from app.service.db import db
from app.utils.helpers import get_data_to_generate

preview_blueprint = Blueprint('preview', __name__)
add_invoice_blueprint = Blueprint('add_invoice', __name__)
download_blueprint = Blueprint('download', __name__)


@preview_blueprint.route('/preview/<id>', methods=['POST'])
@login_required
def preview(id):
    if request.method == "POST":
        generated_inv = User.invoice.query.get(id)
        data = get_data_to_generate(generated_inv)
        return render_template('preview.html', invid=generated_inv.id, client_name=data.client.name,
                               product_name=data.product.product_name, unit_price=data.product.price,
                               postal_code=data.client.postal_code, street=data.client.street,
                               quantity=generated_inv.quantity, date=generated_inv.invoice_date, inv_date=date.today(),
                               total_price=generated_inv.total_price)


@add_invoice_blueprint.route('/add', methods=["POST", "GET"])
@login_required
def add_invoice():
    form = InvoiceForm()
    if 'login' in session:
        user = session['login']
        user = User.query.filter_by(login=user).first()

        form.products_query.query = Product.query.filter_by(user_product_id=user.id)
        form.contractors_query.query = Contractor.query.filter_by(user_contractor_id=user.id)

        if form.validate_on_submit():
            new_invoice = Invoice(amount=form.products_query.data.price, items_quantity=form.quantity.data)

            db.session.add(new_invoice)
            db.session.commit()
            return redirect(url_for('dashboard.dashboard'))
        return render_template('add_invoice.html', form=form)


@download_blueprint.route('/download/<id>', methods=["POST"])
def download_pdf(id):
    if request.method == "POST":
        generated_inv = Invoice.query.get(id)
        data = get_data_to_generate(generated_inv)
        try:
            rendered_pdf = render_template('download_pdf.html', invid=generated_inv.id, client_name=data.client.name,
                                           product_name=data.product.product_name, unit_price=data.product.price,
                                           postal_code=data.client.postal_code, street=data.client.street,
                                           quantity=generated_inv.quantity, date=generated_inv.invoice_date,
                                           inv_date=date.today(),
                                           total_price=generated_inv.total_price)
            html = HTML(string=rendered_pdf)
            generated_pdf = html.write_pdf()
            return send_file(
                io.BytesIO(generated_pdf),
                attachment_filename=f'Test_invoice.pdf'
            )
        except Exception as e:
            flash(e, 'error')

    return redirect(url_for('view.view'))
