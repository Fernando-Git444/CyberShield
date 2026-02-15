from flask import Blueprint

cyber_news_bp = Blueprint('cyber_news', __name__)

from . import routes
