from wtforms import validators, StringField, SubmitField, FloatField
from flask_wtf import FlaskForm


class ProductForm(FlaskForm):
    name = StringField('Product name', validators.Length(min=1, max=75))
    description = StringField('Product description', validators.Length(min=1, max=350))
    pkwiu = StringField('PKWIU', validators.Length(min=10, max=10))
    cn = StringField('CN', validators.Length(min=8, max=8))
    price = FloatField('Price')
    submit = SubmitField('Add')
