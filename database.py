from datetime import date
from . import db


class Invoice(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Float, nullable=False)
    invoice_date = db.Column(db.DateTime, default=date.today(), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('invoice._id'), nullable=False)

    def __init__(self, invoice_date: date, quantity: int, client_id: int, total_price: int):
        self.total_price = total_price
        self.invoice_date = invoice_date
        self.quantity = quantity
        self.client_id = client_id

    @property
    def id(self):
        return self._id


class Clients(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    postal_code = db.Column(db.String(5), nullable=False)
    street = db.Column(db.String(40), nullable=False)

    def __init__(self, name: str, postal_code: str, street: str):
        self.name = name
        self.postal_code = postal_code
        self.street = street

    @property
    def id(self):
        return self._id


class Product(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(300), nullable=False)
    price = db.Column(db.Float, nullable=False)
    invoice_id = db.Column(db.Integer, db.ForeignKey('product._id'), nullable=False)

    def __init__(self, product_name: str, price: float, invoice_id: int):
        self.product_name = product_name
        self.price = price
        self.invoice_id = invoice_id


class Admins(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(30), nullable=False)

    def __init__(self, user, password):
        self.user, self.password = user, password
