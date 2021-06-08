from .database import Clients, Invoice, Product
from . import db
from datetime import date
from collections import namedtuple


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
    delete_invoice(invoice_object)
    delete_client(invoice_object)
