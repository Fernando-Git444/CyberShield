from flask import render_template
from . import safe_scanner_bp

@safe_scanner_bp.route('/safe-scanner')
def index():
    return render_template('safe_scanner/index.html')
