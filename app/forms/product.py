from wtforms import validators, StringField, SubmitField, FloatField
from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField
from app.models.product import Product

def product_query():
    return Product.query

class ProductForm(FlaskForm):
    name = StringField('Product name', [validators.Length(min=1, max=75)])
    description = StringField('Product description', [validators.Length(min=1, max=350)])
    pkwiu = StringField('PKWIU', [validators.Length(min=10, max=10)])
    cn = StringField('CN', [validators.Length(min=8, max=8)])
    price = FloatField('Price')
    submit = SubmitField('Add')
    product_query = QuerySelectField(query_factory=product_query, allow_blank=False, get_label='name, company_name')