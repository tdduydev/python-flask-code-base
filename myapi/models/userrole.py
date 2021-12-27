from myapi.extensions import db
from myapi.models.role import Role
from myapi.models.user import User


class UserWithRole(db.Model):
    __tablename__ = "User_Roles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey("Users.id"), nullable=False)
    role_id = db.Column(db.ForeignKey("Roles.id"), nullable=False)

    def __init__(self,  user_id: int = None,
                 role_id: int = None):
        self.user_id = user_id
        self.role_id = role_id

    def __str__(self) -> str:
        return f"User= {self.user.first_name} {self.user.last_name}, Role= {self.role.name}"

    def __repr__(self) -> str:
        return f"<UserWithRole {self.user.first_name} {self.user.last_name} {self.role.name}>"
