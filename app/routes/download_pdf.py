import io
from datetime import date

from flask import Blueprint, request, render_template, send_file, flash, redirect, url_for
from weasyprint import HTML


from app.utils.helpers import get_data_to_generate

download_pdf_blueprint = Blueprint('download_pdf', __name__)


@download_pdf_blueprint.route('/download_pdf/<id>', methods=["POST"])
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
