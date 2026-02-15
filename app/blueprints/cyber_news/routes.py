from flask import render_template
from . import cyber_news_bp

@cyber_news_bp.route('/cyber-news')
def index():
    return render_template('cyber_news/index.html')
