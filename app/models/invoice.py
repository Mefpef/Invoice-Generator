import datetime
from app.service.db import db



class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    invoice_date = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    items_quantity = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    product_invoice_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)