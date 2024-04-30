# CODE PROVIDED AS TEMPLATE BY TEACHER, then modified to fit my project
# CHATGPT used to debug this code
import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource

from model.users import User

user_api = Blueprint('user_api', __name__,
                   url_prefix='/api/users')


api = Api(user_api)

class UserAPI:        
    # authenticate user
    class _Security(Resource):
        def post(self):
            try:
                body = request.get_json()
                if not body:
                    return {
                        "message": "Please provide user details",
                        "data": None,
                        "error": "Bad request"
                    }, 400
                
                uid = body.get('uid')
                if uid is None:
                    return {'message': f'User ID is missing'}, 400
                password = body.get('password')
                
                user = User.query.filter_by(_uid=uid).first()
                if user is None or not user.is_password(password):
                    return {'message': f"Invalid user id or password"}, 400
                if user:
                    try:
                        token_payload = {
                            "_uid": user._uid,
                        }
                        token = jwt.encode( # encode password
                            token_payload,
                            current_app.config["SECRET_KEY"],
                            algorithm="HS256"
                        )
                        resp = Response("Authentication for %s successful" % (user._uid))
                        resp.set_cookie("jwt", token,
                                max_age=3600,
                                secure=True,
                                httponly=True,
                                path='/',
                                samesite='None'
                                )
                        return resp
                    except Exception as e: # user couldn't be authenicated
                        return {
                            "error": "Something went wrong",
                            "message": str(e)
                        }, 500
                return {
                    "message": "Error fetching auth token!",
                    }, 404
            except Exception as e:
                return {
                        "message": "Something went wrong!",
                        "error": str(e),
                        "data": None
                }, 500
    
    # authenticate the user if the user was found
    class Login(Resource):
        def post(self):
            data = request.get_json()

            uid = data.get('uid')
            password = data.get('password')

            if not uid or not password:
                response = {'message': 'Invalid creds'}
                return jsonify(response)

            user = User.query.filter_by(_uid=uid).first() # get the user from DB

            if user and user.is_password(password):
         
                response = {
                    'message': 'Logged in successfully',
                    'user': {
                        'name': user.name,  
                        'id': user.id
                    }
                }
                return jsonify(response), 200

            response = {'message': 'Invalid id or pass'}
            return jsonify(response), 401
        
    # create a new user based off user info inputted from frontend
    class _Create(Resource):
        def post(self, body):
            name = body.get('name')
            uid = body.get('uid')
            password = body.get('password')
            if uid is not None:
                new_user = User(name=name, uid=uid, password=password) # create user from inputted info
            user = new_user.create()
            if user:
                return user.read()
            return {'message': f'Processed {name}, either a format error or User ID {uid} is duplicate'}, 400
    
    # delete user
    class _Delete(Resource):
        def post(self):

            body = request.get_json()
            uid = body.get('uid')
            password = body.get('password')
            user = User.query.filter_by(_uid=uid).first() # get user from DB based off body info

            if user is None or not user.is_password(password): # make sure user lines up/exists
                return {'message': f'User {uid} not found'}, 404
            json = user.read()
            try:
                user.delete() # delete user
            except Exception:
                return {"error": "User couldn't be deleted"}, 500 # return error if delete didnt work

            return f"Deleted user: {json}", 204 
            
    # build API
    api.add_resource(_Security, '/authenticate')
    api.add_resource(Login, '/login')
    api.add_resource(_Create, '/create')
    api.add_resource(_Delete, '/delete')
