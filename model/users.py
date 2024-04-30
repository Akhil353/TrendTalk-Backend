# Boilerplate code from teacher, then reworked to fit the cpt project
# CHATGPT used to debug this code

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'  # name of DB

    # define the diff. columns of the users DB
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)
    _password = db.Column(db.String(255), unique=False, nullable=False)

    # initialize vars to self
    def __init__(self, name, uid, password="123qwerty"):
        self._name = name
        self._uid = uid
        self.set_password(password)

    # get name
    @property
    def name(self):
        return self._name
    
    # allow for name changing
    @name.setter
    def name(self, name):
        self._name = name
    
    # get user
    @property
    def uid(self):
        return self._uid
    
    # allow for uid changing
    @uid.setter
    def uid(self, uid):
        self._uid = uid
        
    # is the passed uid equal to the actual uid
    def is_uid(self, uid):
        return self._uid == uid
    
    @property
    def password(self):
        return self._password[0:10] + "..." # if password is too long ... is shown

    # create a hashed password for security
    def set_password(self, password):
        self._password = generate_password_hash(password, "pbkdf2:sha256", salt_length=10)

    # make sure password matches hashed password
    def is_password(self, password):
        result = check_password_hash(self._password, password)
        return result
    

    # create the user
    def create(self):
        try:
            db.session.add(self)  # adding user to the DB
            db.session.commit()  # commiting to the DB to be added
            return self
        except IntegrityError:
            db.session.remove() # remove the faulty row
            return {'error': None}

    # reading all info of the user to be shown if needed
    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "uid": self.uid,
        }

    # updating name, username, and password IF a change to that variable is made
    def update(self, name="", uid="", password=""):
        if len(name) > 0:
            self.name = name
        if len(uid) > 0:
            self.uid = uid
        if len(password) > 0:
            self.set_password(password)
        db.session.commit()
        return self

    # delete user based on self
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None



# initialize DB to be used
def initUsers():
    with app.app_context():

        db.create_all()

        # create inital users so the DB isn't empty
        users = [
        User(name='Markiplier', uid='mark', password='iplier'),
        User(name='Mr. Beast', uid='jimmy', password='money'),
        User(name='Mark Rober', uid='science guy', password='flamethrower'),
        User(name='Game Theory', uid='FNAF Fan', password='retired')
        ]

        for user in users: # iterates through users
            try:
                user.create()
            except IntegrityError:
                # removes faulty user if error was recieved
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {user.uid}")
            