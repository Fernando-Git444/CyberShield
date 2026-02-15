from flask import Blueprint

network_sentry_bp = Blueprint('network_sentry', __name__)

from . import routes
