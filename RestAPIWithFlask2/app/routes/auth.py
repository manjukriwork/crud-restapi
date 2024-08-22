from flask import Blueprint, jsonify, request,Flask,current_app
from app.models.user import User
import jwt
from flask_pymongo import PyMongo
from datetime import datetime, timedelta
from app import mongo
from app.utils.jwt import verify_token
from app.routes.user import user_bp
from app.utils.hash import verify_password,hash_password
from werkzeug.security import check_password_hash, generate_password_hash
from app.utils.jwt import generate_token
from werkzeug.security import generate_password_hash
from bson.objectid import ObjectId
from app import mongo
import re
# from app.models.profile import Profile
from datetime import datetime,timedelta

app = Flask(__name__)

auth_bp = Blueprint('auth', __name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/info"
mongo = PyMongo(app)

auth_bp = Blueprint('auth', __name__)



@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    print(data)
    errors = validate_registration_data(data)
    if errors:
        return jsonify({"message": "Invalid data", "errors": errors}), 400

    # Check if the user already exists
    if User.get(data['email']):
        return jsonify({"message": "User already exists"}), 400

    # Proceed with user registration
    # hashed_password = hash_password(data['password'])
    # if not generate_token:
    new_user = {
        "email": data['email'],
        "password": generate_password_hash(data['password']),
        "name": data['name'],
        "dob": data['dob'],
        "age": data['age'],
        "gender": data['gender']
    }
    user_id = current_app.extensions['pymongo'].db.profile.insert_one(new_user).inserted_id

    user_details = {
        "user_id" : user_id,
        "height": data['height'],
        "weight" : data['weight'],
        "phone" : data['phone'],
        "qualification" : data['qualification'],
        "pincode" : data['pincode'],
        "address" : data['address']
    }

    details_id = current_app.extensions['pymongo'].db.users.insert_one(user_details).inserted_id
    # return jsonify({"message": "User created successfully", "user_id": str(user_id),"details_id":str(details_id)}), 201
   
    # token = generate_token(user_id)

    return jsonify({
        "message": "User created successfully",
        "user_id": str(user_id),
        "details_id": str(details_id),
        # "token": token
    }), 201
 


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    print("receive data",  data)
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user_data = User.get(email)
    if not user_data and verify_password :
        return jsonify({"message": "Invalid email or password"}), 400
    user_id = user_data['_id']

    token = generate_token(str(user_data['_id']))
    return jsonify({"message": "Login successful", "token": token})

    
    
@auth_bp.route('/read', methods=['GET'])
def selects():
    # data = request.get_data
    email = request.args.get('email')
    auth_header = request.headers.get('Authorization')
    print(auth_header)
    # email = data.get('email')
    # token = data.get('token')

    if not email :
        return jsonify({'error': 'Email is required'}), 400
    
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({'error': 'Token is required'}), 400

    token = auth_header.split(" ")[1]

    if not verify_token(token):
        return jsonify({"message": "Invalid token"}), 400
    user_data = User.get(email)
    if not user_data:
        return jsonify({"message": "Invalid email"}), 400
    details_data = User.get_user_details(user_data['_id'])
    if not details_data:
        return jsonify({"message": "User details not found"}), 400

    response_data = {
        "email": user_data['email'],
        "name": user_data['name'],
        "dob": user_data['dob'],
        "age": user_data['age'],
        "gender": user_data['gender'],
        "height": details_data['height'],
        "weight": details_data['weight'],
        "phone": details_data['phone'],
        "qualification": details_data['qualification'],
        "pincode": details_data['pincode'],
        "address": details_data['address']
    }

    return jsonify( {"data": response_data}), 200
    # if user:
    #     print(f"Stored hashed password type: {type(user['password'])}")
    #     print(f"Provided password type: {type(password)}")
    # if not user or not verify_password(password, user['password']):
    #     return jsonify({"message": "Invalid credentials"}), 401

    # token = generate_token(user['_id'])
    # return jsonify({"token": token}), 200



def validate_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)

def validate_name(name):
    name_regex = r'^[a-zA-Z\s]+$'
    if re.match(name_regex, name) is None:
        return False
    if len(name) < 2 or len(name) > 50:
        return False
    return True

def validate_password(password):
    password_regex = r'^[a-zA-Z0-9_#$@]+$'
    if re.match(password_regex,password) is None:
        return False
    if len(password) < 2 or len(password) > 50:
        return False
    return True

def validate_dob(dob):
    if not isinstance(dob, str):
        return False
    formats = ['%Y-%m-%d', '%d-%m-%Y', '%d/%m/%Y']
    for fmt in formats:
        try:
            dob_datetime = datetime.strptime(dob, fmt)
            if dob_datetime > datetime.now():
                return False
            return True
        except ValueError:
            continue
    return False

def calculate_age(dob):
    dob_datetime = datetime.strptime(dob, '%Y-%m-%d')
    today = datetime.now()
    age = today.year - dob_datetime.year - ((today.month, today.day) < (dob_datetime.month, dob_datetime.day))
    return age

def validate_age(age, dob=None):
    if not isinstance(age, int) or age < 0 or age > 120:
        return False
    if dob:
        calculated_age = calculate_age(dob)
        if age != calculated_age:
            return False
    return True



def validate_gender(gender):
    return gender in ["Male", "Female", "Other"]

def validate_height(height):
    # Assuming height is in centimeters
    if not isinstance(height, (int, float)) or height <= 0 or height > 300:
        return False
    return True

def validate_weight(weight):
    # Assuming weight is in kilograms
    if not isinstance(weight, (int, float)) or weight <= 0 or weight > 500:
        return False
    return True

def validate_phone(phone):
    phone_regex =  r'^\d{10}$'
    return re.match(phone_regex, phone) is not None

def validate_pincode(pincode):
    pattern = r'^\d{6}$'
    return re.match(pattern, pincode) is not None

def validate_address(address):
    return isinstance(address, str) and len(address) > 0
    
def validate_qualification(qualification):
    return isinstance(qualification, str) and len(qualification) > 0


def validate_registration_data(data):
    required_fields = {
        'email': str,
        'password': str,
        'name': str,
        'dob': str,  # Assuming dob is a string in YYYY-MM-DD format
        'age': int,
        'gender': str,
        'height': (int, float),
        'weight': (int, float),
        'phone': str,
        'qualification': str,
        'pincode': str,
        'address': str
    }
    errors = []
    for field, field_type in required_fields.items():
        if field not in data:
            errors.append(f"Missing field: {field}")
        elif not isinstance(data[field], field_type):
            errors.append(f"Incorrect type for field: {field}. Expected {field_type.__name__ if isinstance(field_type, type) else ' or '.join([t.__name__ for t in field_type])}")
    
    # Additional validation for email format
    if 'email' in data and not validate_email(data['email']):
        errors.append("Invalid email format")                       
     
    # Additional validation for name format and length
    if 'name' in data and not validate_name(data['name']):
        errors.append("Invalid name format or length.")
    
 
    if 'age' in data and not validate_age(data['age'], data.get('dob')):
        errors.append("Invalid age. Age must be a non-negative integer and should match the date of birth if provided.")
    
    # Additional validation for age
    if 'dob' in data and not validate_dob(data['dob']):
        errors.append("Invalid date of birth. ")
                      
    if 'password' in data and not validate_password(data['password']):    
        errors.append("Invalid password")

    if 'gender' in data and not validate_gender(data['gender']):    
        errors.append("Invalid gender")

    if 'height' in data and not validate_height(data['height']) :   
        errors.append("Invalid height")    

    if 'weight' in data and not validate_weight(data['weight'])  :  
        errors.append("Invalid weight")    

    if 'phone' in data and not validate_phone(data['phone'])    :
        errors.append("Invalid phone")    

    if 'address' in data and not validate_address(data['address']):    
        errors.append("Invalid address")    

    if 'pincode' in data and not validate_pincode(data['pincode']) :   
        errors.append("Invalid pincode")    
        
    if 'qualification' in data and not validate_qualification(data['qualification']) :  
        errors.append("Invalid qualification")    

    return errors    