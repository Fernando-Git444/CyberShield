from flask import render_template
from . import identity_guard_bp

@identity_guard_bp.route('/identity-guard')
def index():
    return render_template('identity_guard/index.html')
