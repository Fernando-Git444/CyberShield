from flask import render_template, current_app, flash
from . import cyber_news_bp
import requests

@cyber_news_bp.route('/cyber-news')
def index():
    articles = []
    
    api_key = current_app.config['NEWS_API_KEY']
    
    if not api_key:
        flash("Configura NEWS_API_KEY para ver noticias reales.", "warning")
        # Datos de ejemplo para demostración
        articles = [
            {
                'title': 'Massive Ransomware Attack Hits Global Logistics',
                'description': 'A new variant of ransomware has paralyzed shipping operations worldwide...',
                'source': {'name': 'CyberWire'},
                'url': '#',
                'urlToImage': 'https://via.placeholder.com/150',
                'publishedAt': '2026-02-14T10:00:00Z'
            }
        ]
    else:
        try:
            # Consulta a NewsAPI: noticias recientes sobre ciberseguridad, malware y ransomware
            url = f"https://newsapi.org/v2/everything?q=cybersecurity OR malware OR ransomware&language=en&sortBy=publishedAt&apiKey={api_key}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])[:9] # Mostrar solo las 9 noticias más recientes
            else:
                flash(f"Error cargando noticias: {response.status_code}", "danger")
        except Exception as e:
            flash(f"Error de conexión NewsAPI: {str(e)}", "danger")

    return render_template('cyber_news/index.html', articles=articles)
