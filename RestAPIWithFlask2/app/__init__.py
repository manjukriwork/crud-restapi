from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
# from routes.auth import auth_bp

from bson.objectid import ObjectId




mongo = PyMongo()

# CORS(app)


# app.register_blueprint(auth_bp, url_prefix='/api/auth')


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] ='12345'
    CORS(app)
# Allows all origins

    app.config["MONGO_URI"] = "mongodb://localhost:27017/info"

    mongo.init_app(app)
    # from app.routes import auth # Import routes to register them
    app.extensions = {'pymongo': mongo}
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    return app

#     with app.app_context():
#         app.config['MONGO'] = mongo
#     # Import routes here to avoid circular import
#     from app.routes.auth import auth_bp 
#     from app.routes.user import user_bp

#     # Register blueprints

#     # Register blueprints with prefixes
    app.register_blueprint(user_bp, url_prefix='/api/user')
