from app.service.db import db


class Contractor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    city = db.Column(db.String(150), nullable=False)
    postal_code = db.Column(db.String(5), nullable=False)
    street = db.Column(db.String(40), nullable=False)
    company_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(15))
    email_address = db.Column(db.String(50))
    tax_number = db.Column(db.String(20), nullable=False)
    user_contractor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
