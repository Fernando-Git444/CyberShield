from flask import Blueprint

identity_guard_bp = Blueprint('identity_guard', __name__)

from . import routes
