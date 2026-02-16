from flask import render_template, request, flash, current_app
from . import safe_scanner_bp
import requests
import base64

@safe_scanner_bp.route('/safe-scanner', methods=['GET', 'POST'])
def index():
    scan_result = None
    target_url = None
    
    if request.method == 'POST':
        target_url = request.form.get('url')
        vt_key = current_app.config['VIRUSTOTAL_API_KEY']
        
        if not vt_key:
             flash("Error: VIRUSTOTAL_API_KEY no configurada.", "danger")
        else:
            try:
                # API v3 de VirusTotal - Escáner de URLs
                # 1. Codificar la URL en base64 para generar el identificador
                url_id = base64.urlsafe_b64encode(target_url.encode()).decode().strip("=")
                
                headers = {
                    "accept": "application/json",
                    "x-apikey": vt_key,
                    "content-type": "application/x-www-form-urlencoded"
                }

                # Intentar obtener un reporte existente primero para mayor velocidad
                report_url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
                response = requests.get(report_url, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    attributes = data.get('data', {}).get('attributes', {})
                    scan_result = {
                        'malicious': attributes.get('last_analysis_stats', {}).get('malicious', 0),
                        'harmless': attributes.get('last_analysis_stats', {}).get('harmless', 0),
                        'suspicious': attributes.get('last_analysis_stats', {}).get('suspicious', 0),
                        'total': sum(attributes.get('last_analysis_stats', {}).values()),
                        'reputation': attributes.get('reputation', 0),
                        'last_analysis_date': attributes.get('last_analysis_date', 0)
                    }
                elif response.status_code == 404:
                    # Si no se encontró, se debería enviar a analizar (omitido para evitar complejidad asíncrona en la demo)
                    flash("URL no analizada previamente. Por favor envíala a VirusTotal manualmente para el primer análisis.", "info")
                else:
                    flash(f"Error VirusTotal: {response.status_code}", "warning")

            except Exception as e:
                flash(f"Error de conexión: {str(e)}", "danger")

    return render_template('safe_scanner/index.html', scan_result=scan_result, target_url=target_url)
