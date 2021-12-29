
import json
from typing import List
import functools
from flask.json import jsonify
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import current_user
from myapi.models.role import Role
from myapi.models.user import User
from myapi.models.userrole import UserWithRole
from myapi.permissions import PERMISSION
from myapi.helper.http_code import HttpCode


def update_permissions(old_permission: str):

    # THIS FUNCTION HELP UPDATE THE CURRENT PERMISSION OF THE USER
    # TO THE NEWEST VERSION BASE ON THE permissions.py/PERMISSION
    # BY SYNCHRONIZING THEM
    # TO PREVENT ERROR OR EXCEPTION
    # A TRY CATCH BLOCK IS HERE TO PREVENT THIS FUNCTION FROM CAUSING BIG PROBLEM
    # IF A PROBLEM APPEAR, IT WILL RETURN THE OLD VERSION OF PERMISSION BACK
    try:
        # CONVERT Str TO Dict
        old_permission = json.loads(old_permission)
        # new_permission IS THE NEWEST VERSION PERMISSION
        new_permission = PERMISSION
        for permission_key in new_permission:
            for perm in old_permission[permission_key]:
                if perm in new_permission[permission_key]:
                    new_permission[permission_key][perm] = old_permission[permission_key][perm]
        # CONVERT Dict TO Str
        new_permission = json.dumps(new_permission)
    except:
        return old_permission
    return new_permission


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
            if not user.assigned_roles:
                return {"msg": "NOT PERMMITTED"}, HttpCode.PermissionDenied
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
                    # IF THERE IS NO MATCHED PERMISSION THEN SET FALSE
                    if not permission in permission_dict[permission_field]:
                        PERMITTED = False
                    elif permission_dict[permission_field][permission] == False:
                        PERMITTED = False

                if PERMITTED == True:
                    return fn(*args, **kwargs)

            return {"msg": "NOT PERMMITTED"}, 503
        return decorator
    return wrapper
