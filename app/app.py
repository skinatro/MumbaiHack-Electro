from flask import Flask, request, jsonify
from app.core.config import Config
from app.api.auth import auth_bp
from app.api.encounters import encounters_bp
from app.api.vitals import vitals_bp
from app.api.observations import observations_bp
from app.api.doctors import doctors_bp
from app.api.patients import patients_bp
from app.api.alerts import alerts_bp
import logging
import time
from werkzeug.exceptions import HTTPException
from app.core.utils import api_response

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configure Logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    
    @app.before_request
    def start_timer():
        request.start_time = time.time()
        
    @app.after_request
    def log_request(response):
        if request.path == '/health':
            return response
            
        duration = time.time() - request.start_time
        logger.info(f"{request.method} {request.path} {response.status_code} {duration:.3f}s")
        return response
        
    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return api_response(error=e.description, status_code=e.code)
            
        logger.error(f"Unhandled exception: {e}", exc_info=True)
        return api_response(error="Internal Server Error", status_code=500)
    
    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(encounters_bp)
    app.register_blueprint(vitals_bp)
    app.register_blueprint(observations_bp)
    app.register_blueprint(doctors_bp)
    app.register_blueprint(patients_bp)
    app.register_blueprint(alerts_bp)
    
    @app.route('/health')
    def health():
        return {'status': 'ok'}
        
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
