from src.app import api
from src.apps.user.controllers import UserController, UserObjController

api.add_resource(UserController, '/user/')
api.add_resource(UserObjController, '/user/<int:_id>')
