
# DEFAULT PERMISSIONS
PERMISSION = {
    'user': {
        'create': False,
        'get': True,
        'update': False,
        'edit': False,
        'delete': False
    },
    'role': {
        'create': False,
        'get': True,
        'update': False,
        'delete': False,
        'assign_role': False,
        'unassign_role': False
    },
    'auth': {
        'change_password': True,
        'refresh': True,
        'login': True,
        'revoke_access': False,
        'revoke_refresh': False
    }
}
