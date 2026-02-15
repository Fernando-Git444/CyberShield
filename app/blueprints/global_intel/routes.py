from flask import render_template
from . import global_intel_bp

@global_intel_bp.route('/global-intel')
def index():
    return render_template('global_intel/index.html')
