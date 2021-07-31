from flask import Blueprint, url_for
from flask import current_app

from src.elastic import es

blog = Blueprint('blog', __name__)


@blog.route('/')
def index():
    rtn = ['try this urls:']
    with current_app.test_request_context():
        rtn.append(url_for('blog.create_index', es_index='sample'))
        rtn.append(url_for(
            'blog.set_in_index',
            es_index='sample',
            body='{"first_name": "ehsan", "last_name": "ahmadi"}'
        ))
        rtn.append(url_for('blog.get_from_index', es_index='sample', id=1))
        rtn.append(url_for('blog.get_all_from_index', es_index='sample'))

    return str(rtn)


@blog.route('/create/<string:es_index>')
def create_index(es_index):
    return es.indices.create(index=es_index, ignore=400)


@blog.route('/set/<string:es_index>/<string:body>')
def set_in_index(es_index, body):
    return es.index(index=es_index, body=dict(body))


@blog.route('/get/<string:es_index>/<int:id>')
def get_from_index(es_index, id):
    return es.get(index=es_index, id=id)


@blog.route('/get/<string:es_index>')
def get_all_from_index(es_index):
    return es.search(index=es_index, body={"query": {"match_all": {}}})
