from flask import render_template
from . import risk_engine_bp

@risk_engine_bp.route('/risk-engine')
def index():
    return render_template('risk_engine/index.html')
