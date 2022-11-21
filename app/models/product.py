from app.service.db import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(75), nullable=False)
    description = db.Column(db.String(325))
    pkwiu = db.Column(db.String(10))
    cn = db.Column(db.String(8))
    price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    invoice = db.relationship('Invoice', backref='product')