from typing import cast
from sqlalchemy.ext.hybrid import hybrid_property
import datetime
from sqlalchemy.sql.expression import true
from myapi.extensions import db, pwd_context
from flask_jwt_extended import current_user
from flask_seeder import Seeder, Faker, generator
from sqlalchemy.dialects import postgresql
from sqlalchemy import event, func , Index


class User(db.Model):
    """Basic user model"""
    __tablename__ = "Users"

    #PROPERTIES
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=True)
    _password = db.Column("password", db.String(255), nullable=False)
    last_name = db.Column(db.String(80), nullable=True)
    first_name = db.Column(db.String(80), nullable=True)
    address = db.Column(db.String(80), nullable=True)
    phone = db.Column(db.String(12), nullable=True)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=True )
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=True )
    deleted_at = db.Column(db.TIMESTAMP, nullable=True )

    #RELATIONSHIPS
    assigned_roles = db.relationship("UserWithRole", backref="user", lazy = "joined")
    
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
        self.last_name = lastname
        self.first_name = firstname
        self.address = address
        self.phone = phonenumber

    def __str__(self):
        return "ID=%d, userName=%s, Email=%s, passWord=%s, last_name=%s, first_name=%s, address=%s, phone=%s" % \
               (self.id, self.username, self.email, self._password, self.last_name, self.first_name, self.address,
                self.phone)

    def create_tsvector(*args):
        exp = args[0]
        for e in args[1:]:
            exp += ' ' + e
        return func.to_tsvector('english', exp)

    __ts_vector__ = create_tsvector(
        cast(func.coalesce(first_name, ''), postgresql.TEXT)
    )

    __table_args__ = (
        Index(
            'idx_user_fts',
            __ts_vector__,
            postgresql_using='gin'
        ) ,
    )

#TRIGGERS
@event.listens_for(User, "before_update")
def on_update_trigger(mapper,connection,target):
    table = User.__table__
    target.updated_at = datetime.datetime.now()
