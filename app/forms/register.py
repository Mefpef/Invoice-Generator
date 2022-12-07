from wtforms import Form, PasswordField, validators, StringField, SubmitField
from flask_wtf import FlaskForm

class RegisterForm(FlaskForm):
    login = StringField('Login', [validators.Length(min=1, max=10)], render_kw={"placeholder": "Login"})
    password = PasswordField('Password', [validators.Length(min=6, max=25)])
    submit = SubmitField('Register')