from flask import render_template, current_app, flash
from . import global_intel_bp
import requests
from datetime import datetime, timedelta

@global_intel_bp.route('/global-intel')
def index():
    cves = []
    
    # 1. Fetch Recent Critical CVEs from NVD (National Vulnerability Database)
    # NIST NVD API v2
    try:
        # Get CVEs from the last 30 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        # Format dates as ISO 8601
        pub_start = start_date.strftime('%Y-%m-%dT%H:%M:%S.000')
        pub_end = end_date.strftime('%Y-%m-%dT%H:%M:%S.000')
        
        # Request Critical vulnerabilities (cvssV3Severity=CRITICAL)
        nvd_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        params = {
            'pubStartDate': pub_start,
            'pubEndDate': pub_end,
            'cvssV3Severity': 'CRITICAL',
            'resultsPerPage': 5
        }
        
        # NVD requires an API key for higher rate limits, but works without one slowly.
        # Ideally add apiKey headers if available in config.
        # headers = {'apiKey': current_app.config['NVD_API_KEY']}
        
        response = requests.get(nvd_url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            vulnerabilities = data.get('vulnerabilities', [])
            for item in vulnerabilities:
                cve = item.get('cve', {})
                # Extract relevant fields
                cve_id = cve.get('id')
                description = cve.get('descriptions', [{}])[0].get('value', 'No description')
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
             flash(f"NVD API Warning: Status {response.status_code}", "warning")

    except Exception as e:
        flash(f"Error conectando con NVD: {str(e)}", "danger")

    return render_template('global_intel/index.html', cves=cves)
