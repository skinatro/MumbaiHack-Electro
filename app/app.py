from flask import Flask
from app.core.config import Config
from app.api.auth import auth_bp
from app.api.encounters import encounters_bp
from app.api.vitals import vitals_bp
from app.api.observations import observations_bp
import logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configure Logging
    logging.basicConfig(level=logging.INFO)
    
    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(encounters_bp)
    app.register_blueprint(vitals_bp)
    app.register_blueprint(observations_bp)
    
    @app.route('/health')
    def health():
        return {'status': 'ok'}
        
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
