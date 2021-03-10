import sqlite3
from db import db

#create class to save security.py users-list information in this form
class UserModel(db.Model):
    #tell SQLAlchemy the tablename where these models are going to be stored 
    __tablename__ = 'users' 

    #tell SQLAlchemy what columns the table should/does contain --> the columns that this model is going to have
    #NOTE: these column names need to match Class/Model parameters in order to be saved
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password): #_id, 
        # self.id = _id #id can be deleted as it auto-increments and SQLAlchemy takes care of that automatically
        self.username = username
        self.password = password
        #e.g. if: "self.something = something" was given --> that would not be saved as it is not passed as a db column (see above)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    #function to retrieve info from db
    @classmethod #add this in order to use cls() instead of User() to create User-object below (and =cls instead of self in function)
    def find_by_username(cls, username):
        #return User-object or None
        return cls.query.filter_by(username = username).first()

        #function to retrieve info from db
    @classmethod #add this in order to use cls() instead of User() to create User-object below (and =cls instead of self in function)
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()