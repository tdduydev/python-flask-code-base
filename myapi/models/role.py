from enum import unique
from flask_seeder.generator import String
from sqlalchemy.orm import backref
from myapi.extensions import db
from sqlalchemy import DDL,event
import datetime

class Role(db.Model):
    __tablename__ = "Roles"

    #PROPERTIES
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique = True , nullable = False)
    permissions = db.Column(db.Text, nullable = True, )
    description = db.Column(db.Text, nullable = True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=True )
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=True )
    deleted_at = db.Column(db.TIMESTAMP, nullable=True )

    #RELATIONSHIPS
    assigned_roles = db.relationship("UserWithRole", backref="role", lazy = "joined")


    def __repr__(self) -> str:
        return f"<Role {self.name}>"
    
    def __init__(self,  name: str = None,
                        permissions: str = None,
                        description: str = None) -> None:
        self.name = name
        self.permissions = permissions
        self.description = description

    def __str__(self) -> String:
        return f"name={self.name}, permission={self.permissions}, description={self.description}"

#TRIGGERS
@event.listens_for(Role, "before_update")
def on_update_trigger(mapper,connection,target):
    table = Role.__table__
    target.updated_at = datetime.datetime.now()

@event.listens_for(Role, "before_insert")
def before_insert_trigger(mapper,connection,target):
    target.name = "TraiTran"
