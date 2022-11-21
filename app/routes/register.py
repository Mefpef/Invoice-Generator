from flask import Blueprint

register_blueprint = Blueprint('register', __name__)


@register_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    pass
