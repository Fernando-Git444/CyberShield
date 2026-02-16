import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuración central de la aplicación. Lee las claves desde variables de entorno."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change'
    SUPABASE_URL = os.environ.get('SUPABASE_URL')
    SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
    
    # Claves de APIs por módulo
    HIBP_API_KEY = os.environ.get('HIBP_API_KEY')
    VIEWDNS_API_KEY = os.environ.get('VIEWDNS_API_KEY')
    VIRUSTOTAL_API_KEY = os.environ.get('VIRUSTOTAL_API_KEY')
    GOOGLE_SAFE_BROWSING_KEY = os.environ.get('GOOGLE_SAFE_BROWSING_KEY')
    ALIENVAULT_API_KEY = os.environ.get('ALIENVAULT_API_KEY')
    NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
