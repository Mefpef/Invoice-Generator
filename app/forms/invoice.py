from wtforms import validators, StringField, SubmitField, FloatField, DateField
from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField

from app.models.product import Product
from app.models.contractor import Contractor

class InvoiceForm(FlaskForm):
    contractor_query = FloatField('Contractor')
    product_query = DateField('Product')