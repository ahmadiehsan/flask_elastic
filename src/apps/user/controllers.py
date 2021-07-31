from src.apps.user.models import User
from src.apps.user.schemas import user_schema, users_schema
from src.db import db_session
from src.helpers.controllers import (
    GenericObjController,
    GenericController,
    ListMixin,
    CreateMixin,
    RetrieveMixin,
    UpdateMixin
)


class UserController(GenericController, ListMixin, CreateMixin):
    schema_list = users_schema
    schema_create = user_schema
    query = db_session.query(User)
    model = User


class UserObjController(GenericObjController, RetrieveMixin, UpdateMixin):
    schema_retrieve = user_schema
    query = db_session.query(User)
    model = User
