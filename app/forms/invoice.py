
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms_sqlalchemy.fields import QuerySelectField

from app.models.contractor import Contractor
from app.models.product import Product


def contractor_query():
    return Contractor.query


def product_query():
    return Product.query


class InvoiceForm(FlaskForm):
    quantity = StringField()
    contractors_query = QuerySelectField(query_factory=contractor_query, allow_blank=False,
                                         get_label=lambda s: '%s %s, %s, %s %s' % (
                                         s.name, s.last_name, s.company_name, s.street, s.postal_code))
    products_query = QuerySelectField(query_factory=product_query, allow_blank=False, get_label=lambda s: '%s, %s' % (s.name, str(s.price)+ 'pln'))
    submit = SubmitField('Save Invoice')