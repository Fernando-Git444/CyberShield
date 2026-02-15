from flask import Blueprint

global_intel_bp = Blueprint('global_intel', __name__)

from . import routes
