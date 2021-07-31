import bcrypt
from marshmallow import Schema, fields
from marshmallow.validate import Length, Regexp

from src.config import get_config


class PasswordField(fields.Str):
    def _deserialize(self, value, attr, data, **kwargs):
        return super()._deserialize(value, attr, data, **kwargs)
        return str(bcrypt.hashpw(str.encode(result), bcrypt.gensalt()))


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = PasswordField(
        required=True,
        load_only=True,
        validate=[
            Length(min=8, max=36),
            Regexp(regex=get_config().PASSWORD_PATTERN)
        ]
    )
    create_time = fields.DateTime(dump_only=True, format='%d %b %Y, %H:%M')
    update_time = fields.DateTime(dump_only=True, format='%d %b %Y, %H:%M')


user_schema = UserSchema()
users_schema = UserSchema(many=True)
