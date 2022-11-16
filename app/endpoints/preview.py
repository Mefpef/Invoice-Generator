from collections import namedtuple
from app.models import Invoice, Clients, Product
from flask import Blueprint, render_template

preview_blueprint = Blueprint('preview', __name__)

@preview_blueprint.route('/preview', methods=['GET', 'POST'])
def view():
    invoices = Invoice.query.all()

    TripleData = namedtuple('Invoice_Data', 'invoice client product')
    tuples = []
    for invoice in invoices:
        associated_client = Clients.query.get(invoice.client_id)
        associated_product = Product.query.filter_by(invoice_id=invoice.id).first()

        tuples.append(TripleData(invoice, associated_client, associated_product))

    return render_template('view.html', tuples=tuples)