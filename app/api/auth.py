from flask import Blueprint, request
from app.core.database import get_db
from app.repositories.user_repo import UserRepository
from app.core.security import verify_password, create_access_token, login_required
from app.schemas.auth import LoginRequest, TokenResponse
from app.core.utils import api_response
from pydantic import ValidationError

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return api_response(error="No input data provided", status_code=400)
        req = LoginRequest(**data)
    except ValidationError as e:
        return api_response(error=e.errors(), status_code=400)

    db = next(get_db())
    user = UserRepository.get_by_username(db, req.username)
    
    if not user or not verify_password(user.password_hash, req.password):
        return api_response(error='Invalid credentials', status_code=401)
        
    token = create_access_token({'sub': user.username, 'role': user.role, 'user_id': user.id})
    return api_response(data=TokenResponse(access_token=token).model_dump())

@auth_bp.route('/me', methods=['GET'])
@login_required()
def me():
    return api_response(data=request.current_user)
