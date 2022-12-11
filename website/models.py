from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    __tablename__ = "notes"
    id = db.Column("id",db.Integer, primary_key=True)
    data = db.Column("data", db.String(10000))
    date = db.Column("date", db.DateTime(timezone=True), default=func.now())
    user_id = db.Column("user_id", db.Integer, db.ForeignKey('user.id'))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    def __init__(self, data, user_id):
        self.data = data
        # self.date = date
        self.user_id = user_id
    
    def is_authenticated(self):
        return True

    def is_active(self):   
        return True           

    def is_anonymous(self):
        return False          

    def get_id(self):         
        return str(self.id)    
    
    def __repr__(self):
        return '' % self.id    

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column("id", db.Integer, primary_key=True)
    email = db.Column("Emailadd", db.String(150), unique=True)
    password = db.Column("password", db.String(150))
    firstname = db.Column("firstname", db.String(150))
    notes = db.relationship('Note',backref="user", lazy='dynamic',
                        primaryjoin="User.id == Note.user_id")
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    def __init__(self, email, password, firstname):
        self.firstname = firstname
        self.email = email
        self.password = password
    
    def is_authenticated(self):
        return True

    def is_active(self):   
        return True           

    def is_anonymous(self):
        return False          

    def get_id(self):         
        return str(self.id)
        
    def __repr__(self):
        return '' % self.id
    