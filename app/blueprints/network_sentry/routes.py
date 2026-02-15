from flask import render_template, request, current_app, flash
from . import network_sentry_bp
import requests
import socket

@network_sentry_bp.route('/network-sentry')
def index():
    # If running locally, request.remote_addr is 127.0.0.1, so we need to fetch public IP via an external service
    user_ip = "127.0.0.1" 
    ip_data = {}
    shodan_data = None
    
    try:
        # 1. Get Public IP and Geo Data via IP-API (Free, no key)
        response = requests.get('http://ip-api.com/json/')
        if response.status_code == 200:
            ip_data = response.json()
            user_ip = ip_data.get('query', user_ip)
    except Exception as e:
        flash(f"Error obteniendo IP pública: {str(e)}", "warning")

    # 2. Check Shodan for open ports on this IP
    shodan_key = current_app.config['SHODAN_API_KEY']
    if shodan_key:
        try:
            shodan_url = f"https://api.shodan.io/shodan/host/{user_ip}?key={shodan_key}"
            shodan_res = requests.get(shodan_url)
            if shodan_res.status_code == 200:
                shodan_data = shodan_res.json()
            elif shodan_res.status_code == 404:
                # 404 in Shodan means "No open ports found" -> This is GOOD for security
                shodan_data = {"ports": [], "data": []}
                flash("Excelente: Shodan no encontró puertos expuestos en tu IP.", "success")
        except Exception as e:
            flash(f"Error conectando con Shodan: {str(e)}", "danger")
    else:
         flash("Nota: Configura SHODAN_API_KEY para ver puertos abiertos.", "info")

    return render_template('network_sentry/index.html', ip_data=ip_data, shodan_data=shodan_data, user_ip=user_ip)
