from flask import Flask

from app.routes.home import index_blueprint
from app.routes.products import add_product_blueprint
from app.routes.invoices import preview_blueprint, add_invoice_blueprint, download_blueprint
from app.routes.user import login_blueprint, register_blueprint, dashboard_blueprint, logout_blueprint
from app.service.db import db
from app.utils.login_auth import login_manager

app = Flask(__name__)

app.register_blueprint(index_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(logout_blueprint)
app.register_blueprint(register_blueprint)
app.register_blueprint(dashboard_blueprint)
app.register_blueprint(add_invoice_blueprint)
app.register_blueprint(preview_blueprint)
app.register_blueprint(download_blueprint)
app.register_blueprint(add_product_blueprint)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
login_manager.init_app(app)
login_manager.login_view = 'previews.view'
app.secret_key = b'_5#y2L"F4Q8z/nxec'

db.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8282, debug=True)
