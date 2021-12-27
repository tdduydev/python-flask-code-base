
import json
from typing import List
import functools
from flask.json import jsonify
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import current_user
from myapi.models.role import Role
from myapi.models.user import User
from myapi.models.userrole import UserWithRole


def permissions_required(permission_field: str, permission_names: List[str] = None):
    def wrapper(fn):
        @functools.wraps(fn)
        def decorator(*args, **kwargs):
            # VALID THAT JWT EXIST
            verify_jwt_in_request()

            # GET THE CURRENT USER
            user: User = current_user

            # IF USER IS A SUPER ADMIN THEN PERMIT ALL REQUEST
            if user.is_super_admin == True:
                return fn(*args, **kwargs)
            # LOOP THROUGH CURRENT USER ROLES
            for user_role in user.assigned_roles:
                PERMITTED = True  # CHECK IF ALL PERMISSIONS ARE PERMITTED
                # DEFINE user_role AS UserWithRole TYPE
                user_role: UserWithRole = user_role
                # GET ALL ASSIGNED ROLES OF THE CURRENT USER
                role = Role.query.filter(Role.id == user_role.role_id).first_or_404()

                # TURN permissions AS JSON INTO Dictionary
                permission_dict = json.loads(role.permissions)
                # LOOP THROUGH THE DEMANDED PERMISSIONS
                for permission in permission_names:

                    if not permission in permission_dict[permission_field]:
                        PERMITTED = False
                    elif permission_dict[permission_field][permission] == False:
                        PERMITTED = False

                if PERMITTED == True:
                    return fn(*args, **kwargs)

            return jsonify(msg="NOT PERMMITTED"), 403
        return decorator
    return wrapper
