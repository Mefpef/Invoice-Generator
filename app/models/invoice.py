from datetime import date
from app.service.db import db


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Float, nullable=False)
    invoice_date = db.Column(db.DateTime, default=date.today(), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)