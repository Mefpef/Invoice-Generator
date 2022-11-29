from flask import Flask

from app.routes.download_pdf import download_pdf_blueprint
from app.utils.login_auth import login_manager
from app.service.db import db
from app.routes.logged import admin_blueprint
from app.routes.login import login_blueprint
from app.routes.register import register_blueprint
from app.routes.home import home_blueprint
from app.routes.invoices import previews_blueprint, preview_blueprint, add_invoice_blueprint, \
    delete_invoice_blueprint

app = Flask(__name__)

app.register_blueprint(home_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(add_invoice_blueprint)
app.register_blueprint(previews_blueprint)
app.register_blueprint(preview_blueprint)
app.register_blueprint(download_pdf_blueprint)
app.register_blueprint(delete_invoice_blueprint)
app.register_blueprint(register_blueprint)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///invoice_generator.sqlite3'
login_manager.init_app(app)
app.secret_key = b'_5#y2L"F4Q8z/nxec'

db.init_app(app)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8282, debug=True)
