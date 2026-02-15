from flask import Blueprint

risk_engine_bp = Blueprint('risk_engine', __name__)

from . import routes
