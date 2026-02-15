from flask import Flask
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register Blueprints
    from app.blueprints.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.blueprints.identity_guard import identity_guard_bp
    app.register_blueprint(identity_guard_bp)

    from app.blueprints.network_sentry import network_sentry_bp
    app.register_blueprint(network_sentry_bp)

    from app.blueprints.safe_scanner import safe_scanner_bp
    app.register_blueprint(safe_scanner_bp)

    from app.blueprints.global_intel import global_intel_bp
    app.register_blueprint(global_intel_bp)

    from app.blueprints.cyber_news import cyber_news_bp
    app.register_blueprint(cyber_news_bp)

    from app.blueprints.risk_engine import risk_engine_bp
    app.register_blueprint(risk_engine_bp)

    @app.route('/')
    def index():
        from flask import render_template
        return render_template('dashboard.html')

    return app
