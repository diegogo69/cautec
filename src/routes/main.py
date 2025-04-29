from flask import Blueprint, render_template
from flask_login import current_user, login_required


main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
@main.route('/inicio')
@login_required
def index():
    return render_template('index.html')
