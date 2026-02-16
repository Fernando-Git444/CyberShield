from flask import render_template, request, flash, current_app
from . import identity_guard_bp
import requests

@identity_guard_bp.route('/identity-guard', methods=['GET', 'POST'])
def index():
    breaches = None
    searched_email = None

    if request.method == 'POST':
        searched_email = request.form.get('email')
        # HIBP requiere una clave API de pago para el servicio completo de brechas.
        # Si no se proporciona clave, se usa el modo simulación para la demostración.
        api_key = current_app.config['HIBP_API_KEY']
        
        if not api_key or api_key == "optional-if-paying":
             flash("Advertencia: No se detectó API Key de HIBP. Usando modo simulación para demostración.", "warning")
             # Datos simulados para demostración (sin clave API)
             breaches = [
                 {'Name': 'LinkedIn', 'BreachDate': '2021-06-21', 'Description': 'Scraped data from 700M users.', 'DataClasses': ['Email addresses', 'Phone numbers', 'Geographic location', 'Job titles']},
                 {'Name': 'Adobe', 'BreachDate': '2013-10-04', 'Description': '153 million accounts breached.', 'DataClasses': ['Email addresses', 'Password hints', 'Passwords', 'Usernames']}
             ]
        else:
            headers = {
                'hibp-api-key': api_key,
                'user-agent': 'CyberShield-Hub'
            }
            # Endpoint de la API para obtener brechas asociadas a una cuenta
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{searched_email}?truncateResponse=false"
            
            try:
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    breaches = response.json()
                elif response.status_code == 404:
                    flash(f"¡Buenas noticias! No se encontraron brechas para {searched_email}", "success")
                    breaches = []
                elif response.status_code == 401:
                    flash("Error de API: Key inválida o no autorizada.", "danger")
                else:
                    flash(f"Error consultando HIBP: {response.status_code}", "danger")
            except Exception as e:
                flash(f"Error de conexión: {str(e)}", "danger")

    return render_template('identity_guard/index.html', breaches=breaches, searched_email=searched_email)
