from flask import render_template, current_app
from . import risk_engine_bp
import random

@risk_engine_bp.route('/risk-engine')
def index():
    # Simulated Risk Calculation based on System Hygiene
    score = 100
    findings = []
    
    # 1. Config Check
    # HackerTarget is always active (no API key needed), so we credit this always.
    findings.append({'text': 'Scanner Nmap Activo (HackerTarget)', 'severity': 'low'})

    if not current_app.config.get('VIRUSTOTAL_API_KEY'):
        score -= 20
        findings.append({'text': 'Safe Scanner Desactivado', 'severity': 'high'})
    else:
        findings.append({'text': 'Scanner de Malware Activo', 'severity': 'low'})

    # 2. Simulated Environment Checks
    score -= random.randint(0, 5) 
    
    # Determine Status
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
