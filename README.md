# 🛡️ CyberShield Hub

**Suite de Ciberseguridad Personal** — Aplicación web modular construida con Flask que integra múltiples APIs externas para ofrecer herramientas de análisis y protección digital en tiempo real.

---

## 📋 Objetivo del Proyecto

CyberShield Hub tiene como objetivo proporcionar a los usuarios una plataforma centralizada de ciberseguridad personal que permite:

- **Monitorear** si sus credenciales han sido comprometidas en filtraciones de datos.
- **Auditar** la seguridad de su conexión a Internet analizando puertos expuestos.
- **Escanear** URLs sospechosas para detectar malware y amenazas.
- **Consultar** vulnerabilidades críticas (CVEs) reportadas a nivel mundial.
- **Informarse** con noticias actualizadas sobre ciberseguridad.
- **Evaluar** el nivel de riesgo general de su entorno digital.

La aplicación demuestra la integración práctica de múltiples APIs REST externas en una arquitectura modular basada en Blueprints de Flask, con autenticación de usuarios mediante Supabase.

---

## 🔌 APIs Utilizadas

| # | API | Módulo | Función | Tipo de Acceso |
|---|-----|--------|---------|----------------|
| 1 | [IP-API](http://ip-api.com) | Network Sentry | Obtiene la IP pública del usuario y datos de geolocalización (ISP, ciudad, país, coordenadas). | Gratuita, sin clave |
| 2 | [ViewDNS.info](https://viewdns.info/api/) | Network Sentry | Realiza escaneo de puertos TCP comunes para detectar servicios expuestos en la IP del usuario. | Gratuita con registro |
| 3 | [Have I Been Pwned (HIBP)](https://haveibeenpwned.com/API/v3) | Identity Guard | Consulta si un correo electrónico ha aparecido en filtraciones de datos conocidas. | De pago (modo simulación incluido) |
| 4 | [VirusTotal API v3](https://www.virustotal.com/) | Safe Scanner | Analiza URLs sospechosas contra más de 70 motores antivirus. | Gratuita con registro |
| 5 | [NVD - NIST](https://nvd.nist.gov/developers/vulnerabilities) | Global Intel | Consulta las vulnerabilidades CVE críticas publicadas en los últimos 30 días. | Gratuita, sin clave |
| 6 | [NewsAPI](https://newsapi.org/) | Cyber News | Obtiene noticias recientes sobre ciberseguridad, malware y ransomware. | Gratuita con registro |
| 7 | [Supabase Auth](https://supabase.com/) | Autenticación | Gestiona el registro, inicio de sesión y cierre de sesión de usuarios. | Gratuita con registro |

---

## 🏗️ Arquitectura del Proyecto

```
CyberShield/
├── run.py                          # Punto de entrada de la aplicación
├── config.py                       # Configuración y variables de entorno
├── requirements.txt                # Dependencias de Python
├── .env.example                    # Plantilla de variables de entorno
├── README.md                       # Este archivo
│
└── app/
    ├── __init__.py                 # Fábrica de la aplicación Flask
    ├── utils/
    │   └── supabase_client.py      # Cliente REST personalizado para Supabase Auth
    ├── blueprints/
    │   ├── auth/                   # Autenticación (Login/Registro/Logout)
    │   ├── identity_guard/         # Verificación de filtraciones (HIBP)
    │   ├── network_sentry/         # Auditoría de red (IP-API + ViewDNS)
    │   ├── safe_scanner/           # Escáner de URLs (VirusTotal)
    │   ├── global_intel/           # Vulnerabilidades CVE (NVD/NIST)
    │   ├── cyber_news/             # Noticias de ciberseguridad (NewsAPI)
    │   └── risk_engine/            # Motor de evaluación de riesgo
    ├── templates/                  # Plantillas HTML (Jinja2)
    └── static/                     # Archivos estáticos (CSS/JS)
```

---

## ⚙️ Requisitos Previos

- **Python 3.8+**
- **pip** (gestor de paquetes de Python)
- Conexión a Internet (para las consultas a las APIs)

---

## 🚀 Instalación y Ejecución

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/CyberShield.git
cd CyberShield
```

### 2. Crear entorno virtual (recomendado)
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Copia el archivo de ejemplo y rellena tus claves:
```bash
cp .env.example .env
```

Edita `.env` con tus API Keys (ver sección de APIs arriba para los enlaces de registro).

### 5. Ejecutar la aplicación
```bash
python run.py
```

Accede a la aplicación en: **http://127.0.0.1:5000**

---

## 🔑 Configuración de API Keys

| Variable | Dónde obtenerla | ¿Obligatoria? |
|----------|----------------|---------------|
| `SUPABASE_URL` | [supabase.com](https://supabase.com) | Sí (para autenticación) |
| `SUPABASE_KEY` | Panel de Supabase → Settings → API | Sí (para autenticación) |
| `VIEWDNS_API_KEY` | [viewdns.info/api](https://viewdns.info/api/) | No (usa modo demo si falta) |
| `VIRUSTOTAL_API_KEY` | [virustotal.com](https://www.virustotal.com/gui/join-us) | No (el módulo no funciona sin ella) |
| `NEWS_API_KEY` | [newsapi.org](https://newsapi.org/register) | No (muestra datos de ejemplo) |
| `HIBP_API_KEY` | [haveibeenpwned.com](https://haveibeenpwned.com/API/Key) | No (usa modo simulación) |

> **Nota:** Los módulos **Global Intel (NVD)** e **IP-API** no requieren clave API.

---

## 📦 Dependencias

```
flask
python-dotenv
requests
gunicorn
flask-cors
```

---

## 🎨 Características de la Interfaz

- Diseño temático **Cyberpunk** con paleta oscura y acentos neón.
- Dashboard central con resumen de estado del sistema.
- Tarjetas interactivas para cada módulo de seguridad.
- Alertas visuales diferenciadas por nivel de riesgo (verde/amarillo/rojo).
- Reportes técnicos con formato de terminal (monospace).

---

## 👤 Autor

Proyecto desarrollado como parte de la materia de desarrollo de aplicaciones web con integración de APIs.

---

## 📄 Licencia

Este proyecto es de uso académico.
