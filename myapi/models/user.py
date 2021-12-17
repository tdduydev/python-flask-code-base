<<<<<<< HEAD
from sqlalchemy.ext.hybrid import hybrid_property
import datetime

from myapi.extensions import db, pwd_context


class User(db.Model):
    """Basic user model"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    _password = db.Column("password", db.String(255), nullable=False)
    lastName = db.Column(db.String(80), nullable=True)
    firstName = db.Column(db.String(80), nullable=True)
    address = db.Column(db.String(80), nullable=True)
    phoneNumber = db.Column(db.String(12), nullable=True)
    active = db.Column(db.Boolean, default=True)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = pwd_context.hash(value)

    def __repr__(self):
        return "<User %s>" % self.username


=======
from sqlalchemy.ext.hybrid import hybrid_property
import datetime

from myapi.extensions import db, pwd_context
from flask_seeder import Seeder, Faker, generator


class User(db.Model):
    """Basic user model"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    _password = db.Column("password", db.String(255), nullable=False)
    lastName = db.Column(db.String(80), nullable=True)
    firstName = db.Column(db.String(80), nullable=True)
    address = db.Column(db.String(80), nullable=True)
    phoneNumber = db.Column(db.String(12), nullable=True)
    active = db.Column(db.Boolean, default=True)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = pwd_context.hash(value)

    def __repr__(self):
        return "<User %s>" % self.username

    def __init__(self, username=None, email=None, _password=None,
                 lastname=None, firstname=None, address=None, phonenumber=None):
        self.username = username
        self.email = email
        self._password = _password
        self.lastName = lastname
        self.firstName = firstname
        self.address = address
        self.phoneNumber = phonenumber

    def __str__(self):
        return "ID=%d, userName=%s, Email=%s, passWord=%s, lastName=%s, firstName=%s, address=%s, phoneNumber=%d" % \
               (self.id, self.username, self.email, self._password, self.lastName, self.firstName, self.address,
                self.phoneNumber)







>>>>>>> main
