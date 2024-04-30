# Boilerplate code from AP CSP teacher, then all functions reworked to fit my project
# CHATGPT used to debug this code
from flask import Blueprint, request, jsonify, current_app
from flask_restful import Api, Resource
import jwt
from auth_middleware import token_required
from model.messages import Message 
from model.users import User

message_api = Blueprint('message_api', __name__, url_prefix='/api/messages')

api = Api(message_api)

class MessageAPI:
    # send messages to database
    class _Send(Resource):
        def post(self, body):
            token = request.cookies.get("jwt")
            uid = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])['_uid'] # get uid from token
            user = User.query.filter_by(uid=uid).first() # Get name of user
            name = user._name
            message = body.get('message')
            likes = body.get('likes')

            if uid != None and message != None:
                new_message = Message(uid=name, message=message, likes=likes) # If user and message exist, create message 
            elif message == None:
                return {'error': 'Message does not contain any content'}, 404
            else:
                return {'error': 'User is not logged in or does not exist'}, 404
            message = new_message.create()

            # return an error if there was a problem with creating the message   
            if message:
                return message.read()
            else:
                return {'error': f'Processed {uid}, either a format error or User ID {uid} is duplicate'}, 400
            
    class _CRUD(Resource):
        # get all current messages
        def get(self, _): 
            messages = Message.query.all() # get all messagse
            json_ready = []
            for message in messages.read():
                json_ready.append(message)
            return jsonify(json_ready)
        
        # update a message
        def put(self):
            body = request.get_json()
            new_message = body.get('new_message')
            old_message = body.get('old_message')
            message = Message.query.filter_by(_message=old_message).first() # index the message based off the message content
            message.message = new_message
            return message.message
        
        def post(self, current_user, Message): 
            body = request.get_json()


            message_content = body.get('message')
            if not message_content:
                return {'message': 'Message content is missing'}, 400


            message = Message(uid=current_user.uid, message=message_content)


            try:
                created_message = message.create()
                return jsonify(created_message.read()), 201
            except Exception as e:
                return {'message': f'Failed to create message: {str(e)}'}, 500
        
    class _Delete(Resource): # Remove column based off info of message
        def delete(self, body):
            token = request.cookies.get("jwt")
            message_id = body.get('message')
            uid = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])['_uid'] # get uid from token
            if not message_id:
                return {'message': 'Message ID is missing'}, 400

            for line in Message.query.all():
                if line.message == message_id and line.uid == uid: # if the message and the user match up
                    message = line
            if not message:
                return {'message': 'Message not found'}, 404

            if message.uid != uid:
                return {'message': 'You are not authorized to delete this message'}, 403

            try:
                message.delete()
                return {'message': 'Message deleted successfully'}, 200
            except Exception as e:
                return {'message': f'Failed to delete message: {str(e)}'}, 500
        
    class _Likes(Resource): # update variable in a specific row/column
        def put(self):
            body = request.get_json()
            message = body.get('message')
            message = Message.query.filter_by(_message=message).first()
            message.likes += 1
            return message.likes

# add function sto api to access them from frontend
api.add_resource(MessageAPI._CRUD, '/')
api.add_resource(MessageAPI._Send, '/send')
api.add_resource(MessageAPI._Delete, '/delete')
api.add_resource(MessageAPI._Likes, '/like') 