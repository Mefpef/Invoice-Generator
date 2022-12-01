from app.service.db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    invoice = db.relationship('Invoice', backref='user')
    product = db.relationship('Product', backref='user_product', lazy='joined')
    contractor = db.relationship('Contractor', backref='user_contractor')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
