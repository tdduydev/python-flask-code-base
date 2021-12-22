from enum import unique
from flask_seeder.generator import String
from myapi.extensions import db
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique = True , nullable = False)
    permissions = db.Column(db.Text, nullable = True, )
    description = db.Column(db.Text, nullable = True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=True )
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), server_onupdate = db.func.current_timestamp(), nullable=True )

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