from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///invoice_generator.sqlite3'
    app.secret_key = b'_5#y2L"F4Q8z/nxec'
    app.permanent_session_lifetime = timedelta(minutes=5)
    db.init_app(app)

    from .main import home_blueprint, login_blueprint, admin_blueprint, invoice_creator_blueprint, view_blueprint,\
        pre_blueprint, download_pdf_blueprint, delete_invoice_blueprint
    app.register_blueprint(home_blueprint)
    app.register_blueprint(login_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(invoice_creator_blueprint)
    app.register_blueprint(view_blueprint)
    app.register_blueprint(pre_blueprint)
    app.register_blueprint(download_pdf_blueprint)
    app.register_blueprint(delete_invoice_blueprint)
    return app
