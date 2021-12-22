from myapi.extensions import db
from myapi.models.role import Role
from myapi.models.user import User

class UserWithRole(db.Model):
    user_id = db.Column(db.ForeignKey("user.id"), primary_key = True)
    role_id = db.Column(db.ForeignKey("role.id"), primary_key = True)
    user = db.relationship("User", lazy = "joined")
    role = db.relationship("Role", lazy = "joined")


    def __init__(self,  user: User = None, 
                        role: Role = None):
        self.user= user
        self.role= role

    def __str__(self) -> str:
        return f"User= {self.user.first_name} {self.user.last_name}, Role= {self.role.name}"

    def __repr__(self) -> str:
        return f"<UserWithRole {self.user.first_name} {self.user.last_name} {self.role.name}>"