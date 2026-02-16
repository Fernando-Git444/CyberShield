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

    # 2. Network Scan via ViewDNS API (Real API with Key)
    # Replaces HackerTarget/Shodan. Requires Registration.
    viewdns_key = current_app.config.get('VIEWDNS_API_KEY')
    ht_data = {"ports": [], "raw_report": ""} # Using same variable names to minimize template changes
    ht_error = None
    
    if not viewdns_key or "your-viewdns-key" in viewdns_key:
         # Fallback to Demo Mode if no key provided
         ht_data = {
                "ports": ["80", "443"],
                "raw_report": f"Starting Port Scan (Demo Mode)\nTarget: {user_ip}\n\nPORT    STATE SERVICE\n80/tcp  open  http\n443/tcp open  https\n\n(DEMO MODE - ADD VIEWDNS_API_KEY TO ENABLE REAL SCAN)"
         }
         flash("Modo Demo Activo: Configura VIEWDNS_API_KEY para escaneos reales.", "info")
    else:
        try:
            # Use ViewDNS Port Scan API
            target_url = f"https://api.viewdns.info/portscan/?host={user_ip}&apikey={viewdns_key}&output=json"
            response = requests.get(target_url)
            
            if response.status_code == 200:
                data = response.json()
                # Debugging showed the key is 'response', not 'portscan'
                scan_results = data.get('response', {}).get('port', [])
                
                # Build report text for the UI
                report_lines = [f"ViewDNS Port Scan Report for {user_ip}", "PORT    STATE SERVICE"]
                
                for item in scan_results:
                    port = item.get('number')
                    status = item.get('status')
                    service = item.get('service')
                    
                    if str(status).lower() == 'open':
                        ht_data["ports"].append(port)
                    
                    report_lines.append(f"{port}/tcp  {status}  {service}")
                
                if not scan_results:
                     report_lines.append("No common ports found or API error.")

                ht_data["raw_report"] = "\n".join(report_lines)

                if not ht_data["ports"]:
                     flash("Escaneo completo: No se detectaron puertos abiertos.", "success")
                else:
                     flash(f"¡Atención! Se detectaron {len(ht_data['ports'])} puertos abiertos.", "warning")
                     
            elif response.status_code == 402: # Limit reached
                 ht_error = "Límite API ViewDNS excedido. Intenta más tarde."
            else:
                ht_error = f"Error ViewDNS API: {response.status_code}"
                
        except Exception as e:
            ht_error = f"Error de conexión Scanner: {str(e)}"
            flash(ht_error, "danger")

    return render_template('network_sentry/index.html', ip_data=ip_data, scan_data=ht_data, user_ip=user_ip, scan_error=ht_error)
