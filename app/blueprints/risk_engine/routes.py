from flask import render_template, current_app
from . import risk_engine_bp
import random

@risk_engine_bp.route('/risk-engine')
def index():
    # Cálculo simulado de riesgo basado en la higiene del sistema
    score = 100
    findings = []
    
    # 1. Verificación de configuración de APIs
    # ViewDNS está activo si se configuró la clave correspondiente
    if current_app.config.get('VIEWDNS_API_KEY'):
        findings.append({'text': 'Escáner de Puertos Activo (ViewDNS)', 'severity': 'low'})
    else:
        findings.append({'text': 'Escáner de Puertos en Modo Demo', 'severity': 'medium'})

    if not current_app.config.get('VIRUSTOTAL_API_KEY'):
        score -= 20
        findings.append({'text': 'Safe Scanner Desactivado', 'severity': 'high'})
    else:
        findings.append({'text': 'Scanner de Malware Activo', 'severity': 'low'})

    # 2. Verificaciones simuladas del entorno (variación aleatoria menor)
    score -= random.randint(0, 5) 
    
    # Determinar nivel de riesgo según la puntuación
    if score >= 85:
        risk_level = "BAJO"
        color = "success"
    elif score >= 50:
        risk_level = "MEDIO"
        color = "warning"
    else:
        risk_level = "ALTO"
        color = "danger"

    return render_template('risk_engine/index.html', score=score, risk_level=risk_level, color=color, findings=findings)
