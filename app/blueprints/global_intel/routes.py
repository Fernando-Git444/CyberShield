from flask import render_template, current_app, flash
from . import global_intel_bp
import requests
from datetime import datetime, timedelta

@global_intel_bp.route('/global-intel')
def index():
    cves = []
    
    # 1. Obtener CVEs Críticos Recientes del NVD (Base de Datos Nacional de Vulnerabilidades)
    # API v2 del NIST NVD
    try:
        # Obtener CVEs de los últimos 30 días
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        # Formatear fechas en ISO 8601
        pub_start = start_date.strftime('%Y-%m-%dT%H:%M:%S.000')
        pub_end = end_date.strftime('%Y-%m-%dT%H:%M:%S.000')
        
        # Solicitar vulnerabilidades con severidad CRÍTICA (cvssV3Severity=CRITICAL)
        nvd_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        params = {
            'pubStartDate': pub_start,
            'pubEndDate': pub_end,
            'cvssV3Severity': 'CRITICAL',
            'resultsPerPage': 20

        }
        
        # NVD requiere una clave API para mayores límites de consultas,
        # pero funciona sin clave a menor velocidad.
        
        response = requests.get(nvd_url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            vulnerabilities = data.get('vulnerabilities', [])
            for item in vulnerabilities:
                cve = item.get('cve', {})
                # Extraer campos relevantes de cada CVE
                cve_id = cve.get('id')
                description = cve.get('descriptions', [{}])[0].get('value', 'Sin descripción')
                metrics = cve.get('metrics', {}).get('cvssMetricV31', [{}])[0].get('cvssData', {})
                score = metrics.get('baseScore', 'N/A')
                vector = metrics.get('vectorString', 'N/A')
                
                cves.append({
                    'id': cve_id,
                    'description': description,
                    'score': score,
                    'vector': vector,
                    'published': cve.get('published', '')[:10]
                })
        else:
             flash(f"Advertencia NVD API: Estado {response.status_code}", "warning")

    except Exception as e:
        flash(f"Error conectando con NVD: {str(e)}", "danger")

    return render_template('global_intel/index.html', cves=cves)
