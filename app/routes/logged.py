from flask import Blueprint, render_template, session, url_for, redirect

from app.utils.helpers import payment_date_counter

admin_blueprint = Blueprint('admin_panel', __name__)

@admin_blueprint.route('/admin_panel', methods=["GET"])
def admin_panel():
    if 'username' in session:
        return render_template("logged.html", username=session['username'], diff=payment_date_counter())
    else:
        return redirect(url_for("login.login"))