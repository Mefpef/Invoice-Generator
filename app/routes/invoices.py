from datetime import date, datetime

from flask import request, Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required

from app.models.user import User
from app.utils.helpers import get_data_to_generate, add_client_to_db, count_total_price, add_invoice_to_db, \
    add_product_to_db, get_actual_date, delete_set

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
def create_invoice():
    if request.method == "POST":
        name = request.form['name']
        postal_code = request.form['postal_code']
        street = request.form['street']

        new_client = User.contractor(name, postal_code, street)
        add_client_to_db(new_client)

        invoice_date = request.form['invoice_date']
        quantity = request.form['quantity']
        invoice_datetime = datetime.strptime(invoice_date, '%Y-%m-%d').date()

        product_name = request.form['product_name']
        price = request.form['price']

        new_invoice = User.invoice(invoice_datetime, quantity, client_id=new_client.id,
                                   total_price=count_total_price(price, quantity))
        add_invoice_to_db(new_invoice)

        new_product = User.product(product_name, price, invoice_id=new_invoice.id)
        add_product_to_db(new_product)
        flash('Invoice added successfully!', 'success')
    return render_template('add_invoice.html', today=get_actual_date())




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
