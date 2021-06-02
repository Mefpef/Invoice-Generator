import io

from flask import render_template, Blueprint, request, url_for, redirect, flash, session, send_file
from .database import Admins, Clients, Invoice, Product
from . import db
import hashlib
from datetime import date, datetime
from collections import namedtuple
from weasyprint import HTML

home_blueprint = Blueprint('home_blueprint', __name__)
login_blueprint = Blueprint('login', __name__)
admin_blueprint = Blueprint('admin_panel', __name__)
invoice_creator_blueprint = Blueprint('create', __name__)
view_blueprint = Blueprint('view', __name__)
pre_blueprint = Blueprint('preview', __name__)
download_pdf_blueprint = Blueprint('download_pdf', __name__)
delete_invoice_blueprint = Blueprint('delete', __name__)


def add_invoice_to_db(new_invoice: Invoice) -> None:
    db.session.add(new_invoice)
    db.session.commit()


def add_product_to_db(new_product: Product) -> None:
    db.session.add(new_product)
    db.session.commit()


def add_client_to_db(new_client: Clients) -> None:
    db.session.add(new_client)
    db.session.commit()


def payment_date_counter() -> int:
    today = date.today()
    payment_day = date(today.year, today.month, 20)
    diff = payment_day - today

    if today.day >= 20:
        payment_day = date(today.year, today.month + 1, 20)
        diff = payment_day - today

    return diff.days


def get_actual_date():
    today = date.today()
    return today.strftime("%d.%m.%Y")


def count_total_price(price, quantity):
    total_price = int(quantity) * int(price)
    return total_price


def get_data_to_generate(generated_inv):
    ToGenerate = namedtuple("Generated_Data", 'product client')

    associated_client = Clients.query.get(generated_inv.id)
    associated_product = Product.query.filter_by(invoice_id=generated_inv.id).first()

    return ToGenerate(product=associated_product, client=associated_client)


def get_template(html, **kwargs):
    return render_template(html, kwargs=kwargs)


def delete_invoice(invoice_object):
    db.session.delete(invoice_object)
    db.session.commit()


def delete_product(invoice_object):
    product_to_delete = Product.query.filter_by(invoice_id=invoice_object.id).first()
    db.session.delete(product_to_delete)
    db.session.commit()


def delete_client(invoice_object):
    client_to_delete = Clients.query.get(invoice_object.client_id)
    db.session.delete(client_to_delete)
    db.session.commit()


def delete_set(inv_id):
    invoice_object = Invoice.query.get(inv_id)
    delete_product(invoice_object)
    delete_client(invoice_object)
    delete_invoice(invoice_object)

@view_blueprint.route('/view', methods=['GET', 'POST'])
def view():
    invoices = Invoice.query.all()

    TripleData = namedtuple('Invoice_Data', 'invoice client product')
    tuples = []
    for invoice in invoices:
        associated_client = Clients.query.get(invoice.client_id)
        associated_product = Product.query.filter_by(invoice_id=invoice.id).first()

        tuples.append(TripleData(invoice, associated_client, associated_product))

    return render_template('view.html', tuples=tuples)


@home_blueprint.route("/")
def home():
    return redirect(url_for("login.login"))


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


@admin_blueprint.route('/admin_panel', methods=["GET"])
def admin_panel():
    if 'username' in session:
        return render_template("admin_panel.html", username=session['username'], diff=payment_date_counter())
    else:
        return redirect(url_for("login.login"))


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


@download_pdf_blueprint.route('/download_pdf/<id>', methods=["POST"])
def download_pdf(id):
    if request.method == "POST":
        generated_inv = Invoice.query.get(id)
        data = get_data_to_generate(generated_inv)
        try:
            rendered_pdf = render_template('testinvoice_pdf.html', invid=generated_inv.id, client_name=data.client.name,
                                           product_name=data.product.product_name, unit_price=data.product.price,
                                           postal_code=data.client.postal_code, street=data.client.street,
                                           quantity=generated_inv.quantity, date=generated_inv.invoice_date)
            html = HTML(string=rendered_pdf)
            generated_pdf = html.write_pdf()
            return send_file(
                io.BytesIO(generated_pdf),
                attachment_filename=f'Invoice dupa.pdf'
            )
        except Exception as e:
            flash(e, 'error')

    return redirect(url_for('view.view'))


@pre_blueprint.route('/preview/<id>', methods=["POST"])
def preview(id):
    if request.method == "POST":
        generated_inv = Invoice.query.get(id)
        data = get_data_to_generate(generated_inv)
        return render_template('preview.html', invid=generated_inv.id, client_name=data.client.name,
                               product_name=data.product.product_name, unit_price=data.product.price,
                               postal_code=data.client.postal_code, street=data.client.street,
                               quantity=generated_inv.quantity, date=generated_inv.invoice_date)


@delete_invoice_blueprint.route('/delete/<id>', methods=['GET'])
def delete(id):
    if request.method == 'GET':
        delete_set(id)

    return redirect(url_for('view.view'))
