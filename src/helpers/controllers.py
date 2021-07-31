from flask import request
from flask_restful import Resource, abort
from flask_restful_swagger import swagger
from marshmallow import ValidationError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from src.db import db_session


class GenericControllerMixin(Resource):
    query = None
    model = None

    def _assert_not_none_field(self, field_name):
        assert getattr(self, field_name) is not None, (
            f'{self.__class__.__name__} should include a `{field_name}` attribute'
        )

    def get_query(self):
        self._assert_not_none_field('query')
        return self.query

    def get_model(self):
        self._assert_not_none_field('model')
        return self.model


class GenericObjController(GenericControllerMixin):
    schema_retrieve = None
    schema_update = None

    def get_obj(self, _id):
        query = self.get_query()
        model = self.get_model()

        try:
            return query.filter(model.id == _id).one()
        except NoResultFound:
            abort(404, error_message=f'not found record with id={_id} form {model.__name__} model')
        except MultipleResultsFound:
            abort(404, error_message=f'found multiple record with id={_id} form {model.__name__} model')

    def get_schema(self):
        method = request.method.lower()

        if method == 'get':
            self._assert_not_none_field('schema_retrieve')
            return self.schema_retrieve

        elif method in ['put', 'patch']:
            self._assert_not_none_field('schema_update')
            return self.schema_update


class GenericController(GenericControllerMixin):
    schema_list = None
    schema_create = None

    def get_schema(self):
        method = request.method.lower()

        if method == 'get':
            self._assert_not_none_field('schema_list')
            return self.schema_list

        elif method in ['post']:
            self._assert_not_none_field('schema_create')
            return self.schema_create


# noinspection PyUnresolvedReferences
class ListMixin:
    @swagger.operation(nickname='list', responseMessages=[{'code': 200}])
    def get(self):
        schema = self.get_schema()
        query = self.get_query()
        return schema.dump(query.all())


# noinspection PyUnresolvedReferences
class CreateMixin:
    @swagger.operation(
        nickname='create',
        parameters=[
            {
                'name': 'body',
                'description': '',
                'required': True,
                'allowMultiple': False,
                'dataType': '',
                'paramType': 'body'
            }
        ],
        responseMessages=[{'code': 201}, {'code': 422}]
    )
    def post(self):
        json_data = request.get_json()
        schema = self.get_schema()

        try:
            validated_data = schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        model = self.get_model()
        instance = model(**validated_data)
        db_session.add(instance)
        db_session.commit()
        return schema.dump(instance)


# noinspection PyUnresolvedReferences
class RetrieveMixin:
    @swagger.operation(nickname='retrieve', responseMessages=[{'code': 200}, {'code': 404}])
    def get(self, _id):
        obj = self.get_obj(_id)
        schema = self.get_schema()
        return schema.dump(obj)


# noinspection PyUnresolvedReferences
class UpdateMixin:
    def _update(self, _id, partial=False):
        json_data = request.get_json()
        schema = self.get_schema()

        try:
            validated_data = schema.load(json_data, partial=partial)
        except ValidationError as err:
            return err.messages, 422

        obj = self.get_obj(_id)
        for attr, value in validated_data.items():
            setattr(obj, attr, value)

        db_session.commit()
        return schema.dump(obj)

    @swagger.operation(
        nickname='put_update',
        parameters=[
            {
                'name': 'body',
                'description': '',
                'required': True,
                'allowMultiple': False,
                'dataType': '',
                'paramType': 'body'
            }
        ],
        responseMessages=[{'code': 200}, {'code': 422}]
    )
    def put(self, _id):
        self._update(_id)

    @swagger.operation(
        nickname='patch_update',
        parameters=[
            {
                'name': 'body',
                'description': '',
                'required': True,
                'allowMultiple': False,
                'dataType': '',
                'paramType': 'body'
            }
        ],
        responseMessages=[{'code': 200}, {'code': 422}]
    )
    def patch(self, _id):
        self._update(_id, True)
