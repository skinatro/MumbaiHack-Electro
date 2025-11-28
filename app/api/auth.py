from flask import Blueprint, request, jsonify
from app.core.database import get_db
from app.repositories.user_repo import UserRepository
from app.core.security import verify_password, create_access_token, login_required

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    db = next(get_db())
    user = UserRepository.get_by_username(db, username)
    
    if not user or not verify_password(user.password_hash, password):
        return jsonify({'error': 'Invalid credentials'}), 401
        
    token = create_access_token({'sub': user.username, 'role': user.role, 'user_id': user.id})
    return jsonify({'access_token': token, 'token_type': 'bearer'})

@auth_bp.route('/me', methods=['GET'])
@login_required()
def me():
    return jsonify(request.current_user)
