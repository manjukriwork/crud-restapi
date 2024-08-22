import jwt
from datetime import datetime,timedelta
from flask_cors import CORS
from flask import current_app
from werkzeug.security import check_password_hash
from flask import Flask, jsonify, request, send_from_directory




app = Flask(__name__)
CORS(app)

SECRET_KEY = '12345'

def generate_token(user_id):
    secret_key = current_app.config['SECRET_KEY']
    if not isinstance(secret_key, str):
        raise TypeError("SECRET_KEY should be a string")
    
    token = jwt.encode({
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=1)
    }, secret_key, algorithm="HS256")
    
    return token
def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
