from datetime import datetime

from flask import request, flash, render_template, Blueprint

from app.models import Clients, Invoice, Product
from app.utils.utils import add_client_to_db, count_total_price, add_invoice_to_db, add_product_to_db, get_actual_date

invoice_creator_blueprint = Blueprint('create', __name__)


@invoice_creator_blueprint.route('/create', methods=["POST", "GET"])
def create_invoice():
    if request.method == "POST":
        name = request.form['name']
        postal_code = request.form['postal_code']
        street = request.form['street']

        new_client = Clients(name, postal_code, street)
        add_client_to_db(new_client)

        invoice_date = request.form['invoice_date']
        quantity = request.form['quantity']
        invoice_datetime = datetime.strptime(invoice_date, '%Y-%m-%d').date()

        product_name = request.form['product_name']
        price = request.form['price']

        new_invoice = Invoice(invoice_datetime, quantity, client_id=new_client.id,
                              total_price=count_total_price(price, quantity))
        add_invoice_to_db(new_invoice)

        new_product = Product(product_name, price, invoice_id=new_invoice.id)
        add_product_to_db(new_product)
        flash('Invoice added successfully!', 'success')
    return render_template('add_invoice.html', today=get_actual_date())
