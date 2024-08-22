from werkzeug.security import generate_password_hash
from flask_pymongo import PyMongo
from flask import current_app as app
mongo = PyMongo()
from bson.objectid import ObjectId
from flask import current_app
from pymongo import MongoClient


# class User:
#     def __init__(self, email, password, name, dob, age, gender, height, weight, phone, qualification, pincode, address):
#         self.email = email
#         self.password = generate_password_hash(password)
#         self.name = name
#         self.dob = dob
#         self.age = age
#         self.gender = gender
#         self.height = height
#         self.weight = weight
#         self.phone = phone
#         self.qualification = qualification
#         self.pincode = pincode
#         self.address = address

    

class User:
        @staticmethod
        def get(email):
            client = MongoClient('localhost', 27017)
            db = client.info
            user_data = db.profile.find_one({"email": email})
            client.close()
            return user_data
        

        
        @staticmethod
        def get_user_details(user_id):
            mongo = current_app.extensions.get('pymongo')
            if mongo is None:
                raise RuntimeError("MongoDB not initialized")
            details_data = mongo.db.users.find_one({"user_id": ObjectId(user_id)})
            return details_data 

        # @staticmethod
        # def create_token(user_id):
        #     return create_access_token(identity=str(user_id))   

    #     @staticmethod
    #     def validate_token(token):
    #         try:
    #             decoded_token = decode_token(token)
    #             return decoded_token['identity']
    #         except Exception as e:
    #             print(f"Token validation error: {e}")
    #             return None    
    # # @classmethod
    # def create_user(cls, data):
    #     result = app.config['MONGO'].db.profile.insert_one(data)
    #     return str(result.inserted_id)
    # def save(self):
    #     user_data= {
    #             "email": self.email,
    #             "password": self.password,
    #             "name": self.name,
    #             "dob": self.dob,
    #             "age": self.age,
    #             "gender": self.gender,
    #             "height": self.height,
    #             "weight": self.weight,
    #             "phone": self.phone,
    #             "qualification": self.qualification,
    #             "pincode": self.pincode,
    #             "address": self.address
    #         }
    #     return self.create_user(user_data)
    
