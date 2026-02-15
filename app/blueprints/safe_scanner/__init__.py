from flask import Blueprint

safe_scanner_bp = Blueprint('safe_scanner', __name__)

from . import routes
