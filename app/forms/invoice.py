
from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField

from app.models.product import Product
from app.models.contractor import Contractor


def product_query():
    return Product.query

def contractor_query():
    return Contractor.query
class InvoiceForm(FlaskForm):
    product_query = QuerySelectField(query_factory=product_query, allow_blank=False, get_label='name')
    contractor_query = QuerySelectField(query_factory=contractor_query, allow_blank=False, get_label='name')

