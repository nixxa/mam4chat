from . import create_app
app = create_app()


import os
app_mode = os.environ.get('APP_MODE', 'DEVEL')
if app_mode == 'DEVEL':
    from .auth import authenticate, identity
    from flask_jwt import JWT
    jwt = JWT(app, authenticate, identity)
