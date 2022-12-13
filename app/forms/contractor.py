from wtforms import validators, StringField, SubmitField, FloatField
from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField
from app.models.contractor import Contractor

def contractor_query():
    return Contractor.query

class ContractorForm(FlaskForm):
    name = StringField('Name', [validators.Length(min=1, max=75)])
    last_name = StringField('Last Name', [validators.Length(min=1, max=75)])
    city = StringField('City', [validators.Length(max=40)])
    postal_code = StringField('Postal Code')
    street = StringField('Street')
    company_name = StringField('Company Name')
    phone_numer = StringField('Phone Number')
    email_address = StringField('E-Mail')
    tax_number = StringField('Tax Number')
    contractors_query = QuerySelectField(query_factory=contractor_query, allow_blank=False, get_label=lambda s: '%s %s, %s, %s %s' % (s.name, s.last_name ,s.company_name, s.street, s.postal_code))