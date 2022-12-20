from werkzeug.security import generate_password_hash, check_password_hash

from app.service.db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    invoice = db.relationship('Invoice', backref='user', lazy=True)
    product = db.relationship('Product', backref='user_product', lazy=True)
    contractor = db.relationship('Contractor', backref='user_contractor', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def is_authenticated(self):
        return True

    @staticmethod
    def is_active(self):
        return True

    @staticmethod
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

