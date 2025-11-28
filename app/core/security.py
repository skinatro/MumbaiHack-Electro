import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.core.config import Config
from functools import wraps
from flask import request, jsonify

def hash_password(password):
    return generate_password_hash(password)

def verify_password(password_hash, password):
    return check_password_hash(password_hash, password)

def create_access_token(data: dict):
    payload = data.copy()
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

def decode_access_token(token):
    try:
        return jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def login_required(roles=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({'error': 'Missing or invalid token'}), 401
            
            token = auth_header.split(' ')[1]
            payload = decode_access_token(token)
            
            if not payload:
                return jsonify({'error': 'Invalid or expired token'}), 401
            
            if roles and payload.get('role') not in roles:
                return jsonify({'error': 'Insufficient permissions'}), 403
                
            request.current_user = payload
            return f(*args, **kwargs)
        return decorated_function
    return decorator
