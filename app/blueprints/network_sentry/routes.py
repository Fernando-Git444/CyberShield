from flask import render_template
from . import network_sentry_bp

@network_sentry_bp.route('/network-sentry')
def index():
    return render_template('network_sentry/index.html')
