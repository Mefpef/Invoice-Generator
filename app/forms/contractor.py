from wtforms import validators, StringField, SubmitField, FloatField
from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField
from app.models.contractor import Contractor

def contractor_query():
    return Contractor.query

class ContractorForm(FlaskForm):
    name = StringField('Name')
    last_name = StringField('Last Name')
    city = StringField('City')
    postal_code = StringField('Postal Code')
    street = StringField('Street')
    company_name = StringField('Company Name')
    phone_numer = StringField('Phone Number')
    email_address = StringField('E-Mail')
    tax_number = StringField('Tax Number')
    contractor_query = QuerySelectField(query_factory=contractor_query, allow_blank=False, get_label='name')