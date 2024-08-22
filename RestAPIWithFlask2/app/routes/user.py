from flask import Blueprint, jsonify, request, current_app as app
from app.models.user import User
from functools import wraps
import jwt
from  app.config import SECRET_KEY
from app.utils.jwt import verify_token
from bson import ObjectId 

from bson import ObjectId  # Import ObjectId from bson package

user_bp = Blueprint('user', __name__)

# Example of a decorator to verify JWT token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        print(token)
        if not token :
            return jsonify({'message': 'Token is missing'}), 401
     
        try:
            data = jwt.decode(token, '12345', algorithms=["HS256"])
            print(SECRET_KEY)
                # 'your_secret_key' should be replaced with the actual secret key used to sign the token

                # Example: Extracting user_id from token
            user_id = data['user_id']

                # Add the user_id or other extracted data to kwargs if needed
            kwargs['user_id'] = user_id
            
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token is expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    return decorated





@user_bp.route('/get_details/<email>', methods=['GET'])
@token_required
def getting_detail(email , user_id = None):
    # token = request.headers.get('Authorization')
    print(email)
    print(user_id)
    # if not token:
    #     return jsonify({'message': 'Token is missing'}), 401
    # else:
    #     verify_tokens=verify_token(token)
    #     print(verify_tokens)
    #     print(email)
    #     if verify_tokens is None:
    #         app.logger.debug(f"Your token is not valid: {email}")
    #         return jsonify({"message" : "Your token is not valid"})
    #     else :
    try:
        _user = User.find_by_email(email)
        if _user:
                    # Convert ObjectId to string for JSON serialization
            _user['_id'] = str(_user['_id'])
            _user['password'] = _user['password'].decode('utf-8')
            return jsonify(_user), 200
        else:
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
                return jsonify({"message": str(e)}), 500

# Example route that requires token authentication
# @api.route('/protected_resource')
# @token_required
# def protected_resource(user_id):
#     return jsonify({'message': f'You have access to protected resource with user ID {user_id}'})
