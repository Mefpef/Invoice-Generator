from app.service.db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    invoice = db.relationship('Invoice', backref='user')
    product = db.relationship('Product', backref='product_')
    contractor = db.relationship('Contractor', backref='users_contractor')