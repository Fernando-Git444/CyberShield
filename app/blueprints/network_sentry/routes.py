from flask import render_template, request, current_app, flash
from . import network_sentry_bp
import requests

@network_sentry_bp.route('/network-sentry')
def index():
    # Si se ejecuta localmente, request.remote_addr es 127.0.0.1,
    # por lo que necesitamos obtener la IP pública mediante un servicio externo
    user_ip = "127.0.0.1" 
    ip_data = {}
    
    try:
        # 1. Obtener IP Pública y Datos de Geolocalización via IP-API (Gratuita, sin clave)
        response = requests.get('http://ip-api.com/json/')
        if response.status_code == 200:
            ip_data = response.json()
            user_ip = ip_data.get('query', user_ip)
    except Exception as e:
        flash(f"Error obteniendo IP pública: {str(e)}", "warning")

    # 2. Escaneo de Red mediante la API de ViewDNS (API Real con Clave)
    # Reemplaza a HackerTarget/Shodan. Requiere registro en viewdns.info
    viewdns_key = current_app.config.get('VIEWDNS_API_KEY')
    ht_data = {"ports": [], "raw_report": ""} # Se mantienen los nombres de variable para compatibilidad con la plantilla
    ht_error = None
    
    if not viewdns_key or "your-viewdns-key" in viewdns_key:
         # Modo Demo: si no se proporciona clave, se muestran datos simulados
         ht_data = {
                "ports": ["80", "443"],
                "raw_report": f"Starting Port Scan (Demo Mode)\nTarget: {user_ip}\n\nPORT    STATE SERVICE\n80/tcp  open  http\n443/tcp open  https\n\n(MODO DEMO - AGREGA VIEWDNS_API_KEY PARA HABILITAR ESCANEO REAL)"
         }
         flash("Modo Demo Activo: Configura VIEWDNS_API_KEY para escaneos reales.", "info")
    else:
        try:
            # Llamada a la API de Escaneo de Puertos de ViewDNS
            target_url = f"https://api.viewdns.info/portscan/?host={user_ip}&apikey={viewdns_key}&output=json"
            response = requests.get(target_url)
            
            if response.status_code == 200:
                data = response.json()
                # La respuesta usa la clave 'response' para los resultados
                scan_results = data.get('response', {}).get('port', [])
                
                # Construir el texto del reporte para la interfaz
                report_lines = [f"Reporte de Escaneo de Puertos ViewDNS para {user_ip}", "PUERTO  ESTADO  SERVICIO"]
                
                for item in scan_results:
                    port = item.get('number')
                    status = item.get('status')
                    service = item.get('service')
                    
                    if str(status).lower() == 'open':
                        ht_data["ports"].append(port)
                    
                    report_lines.append(f"{port}/tcp  {status}  {service}")
                
                if not scan_results:
                     report_lines.append("No se encontraron puertos comunes o error de API.")

                ht_data["raw_report"] = "\n".join(report_lines)

                if not ht_data["ports"]:
                     flash("Escaneo completo: No se detectaron puertos abiertos.", "success")
                else:
                     flash(f"¡Atención! Se detectaron {len(ht_data['ports'])} puertos abiertos.", "warning")
                     
            elif response.status_code == 402: # Límite alcanzado
                 ht_error = "Límite API ViewDNS excedido. Intenta más tarde."
            else:
                ht_error = f"Error ViewDNS API: {response.status_code}"
                
        except Exception as e:
            ht_error = f"Error de conexión con el escáner: {str(e)}"
            flash(ht_error, "danger")

    return render_template('network_sentry/index.html', ip_data=ip_data, scan_data=ht_data, user_ip=user_ip, scan_error=ht_error)
