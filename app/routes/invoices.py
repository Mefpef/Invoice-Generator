from datetime import date, datetime

from flask import request, Blueprint, render_template, flash, redirect, url_for, session
from flask_login import login_required

from app.models.contractor import Contractor
from app.models.user import User
from app.utils.helpers import get_data_to_generate
from app.models.product import Product
from app.forms.contractor import ContractorForm
from app.forms.product import ProductForm
preview_blueprint = Blueprint('preview', __name__)
add_invoice_blueprint = Blueprint('create', __name__)
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
def create_invoice():
    product_form = ProductForm()
    contractor_form = ContractorForm()

    if 'login' in session:
        user = session['login']
        user = User.query.filter_by(login=user).first()

        product_form.product_query.query = Product.query.filter_by(user_product_id=user.id)
        contractor_form.contractor_query.query = Contractor.query.filter_by(user_contractor_id=user.id)

        if product_form.validate_on_submit() and contractor_form.validate_on_submit():
            return redirect(url_for('dashboard.dashboard'))

        return render_template('add_invoice.html', product_form=product_form, contractor_form=contractor_form)
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
