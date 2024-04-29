# boilerplate code provided by teacher, then modified for this project
# CHATGPT used to debug this code
from datetime import date
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError

class Message(db.Model):
    __tablename__ = 'messages'  # table name is pural, class name is singular

    # make the DB columns
    id = db.Column(db.Integer, primary_key=True)
    _uid = db.Column(db.String(255), unique=False, nullable=False)
    _message = db.Column(db.Text, nullable=False)
    _date = db.Column(db.DateTime, nullable=False, default=date.today())
    _likes = db.Column(db.Integer, nullable=False, default=0)
    
    # initialize variables 
    def __init__(self, uid, message, likes, date=date.today()):
        self._uid = uid
        self._message = message
        self._date = date
        self._likes = likes

    # get uid from DB
    @property
    def uid(self):
        return self._uid
    
    # update uid after definition
    @uid.setter
    def is_uid(self, uid):
        self._uid = uid

    # gets message from column
    @property
    def message(self):
        return self._message
    
    # change message in column
    @message.setter
    def message(self, message):
        self._message = message
    
    # gets date from current day
    @property
    def date(self):
        return self._date.strftime('%m-%d-%Y %H:%M:%S')
    
    @property
    def likes(self):
        return self._likes
    
    @likes.setter
    def likes(self, likes):
        self._likes = likes
        db.session.commit()
    
    def create(self):
        try:
            # creates a message object from Message class, goes through initialization
            db.session.add(self)  
            db.session.commit()  # sqlAlchemy needs a commit to add to the DB
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # Reads all the information of a column as dictionary
    def read(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "message": self.message,
            "date": self.date,
            "likes": self.likes
        }

    # updating message content using the old message and new message
    def update(self, old_message, new_message):
        message = Message.query.get(old_message)
        message.message = new_message
        db.session.commit()
        return self

    # Deleting a row
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None
    
    def readMessages(self):
        messages = Message.query.all()
        message_list = []
                
        for message in messages:
            if message.message is not None:
                new_message = {
                    'uid': message.uid,
                    'message': message.message,
                    'likes': message.likes,
                    'date': message.date
                }
            message_list.append(new_message)
        return json.dumps(message_list)

def initMessages():
    with app.app_context():
        db.create_all()
        # preset messages
        m1 = Message(uid='toby', message='Hello from Thomas Edison', likes=3)
        m2 = Message(uid='niko', message='Greetings from Nicholas Tesla', likes=0)
        m3 = Message(uid='lex', message='Welcome from Alexander Graham Bell', likes=27)
        m4 = Message(uid='hop', message='Good day from Grace Hopper', likes=-74)
        messages = [m1, m2, m3, m4]

        # add to db
        for message in messages:
            try:
                message.create()
            except IntegrityError:
                # removes faluty message if error
                db.session.remove()
                print(f"Records exist, duplicate message, or error: {message.uid}")