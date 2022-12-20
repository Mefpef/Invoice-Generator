from flask_wtf import FlaskForm
from wtforms import validators, StringField


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
