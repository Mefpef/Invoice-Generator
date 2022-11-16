import io

from flask import render_template, Blueprint, request, url_for, redirect, flash, session, send_file
from app.models import Admins
import hashlib
from datetime import datetime
from weasyprint import HTML
from app.utils.utils import *
from collections import namedtuple


pre_blueprint = Blueprint('previe', __name__)
download_pdf_blueprint = Blueprint('download_pdf', __name__)
delete_invoice_blueprint = Blueprint('delete', __name__)



@download_pdf_blueprint.route('/download_pdf/<id>', methods=["POST"])
def download_pdf(id):
    if request.method == "POST":
        generated_inv = Invoice.query.get(id)
        data = get_data_to_generate(generated_inv)
        try:
            rendered_pdf = render_template('invoice_pdf.html', invid=generated_inv.id, client_name=data.client.name,
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


@pre_blueprint.route('/previe/<id>', methods=["POST"])
def preview(id):
    if request.method == "POST":
        generated_inv = Invoice.query.get(id)
        data = get_data_to_generate(generated_inv)
        return render_template('preview.html', invid=generated_inv.id, client_name=data.client.name,
                               product_name=data.product.product_name, unit_price=data.product.price,
                               postal_code=data.client.postal_code, street=data.client.street,
                               quantity=generated_inv.quantity, date=generated_inv.invoice_date, inv_date=date.today(),
                               total_price=generated_inv.total_price)


@delete_invoice_blueprint.route('/delete/<id>', methods=['GET'])
def delete(id):
    if request.method == 'GET':
        delete_set(id)

    return redirect(url_for('view.view'))
