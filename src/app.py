from importlib import import_module

from flask import Flask
from flask_restful import Api
from flask_restful_swagger import swagger

from src.apps.blog.controllers import blog
from src.config import get_config
from src.db import db_session

# defining flask app
app = Flask(__name__)
app.config.from_object(get_config())

# defining API
api = swagger.docs(
    Api(app),
    apiVersion='0.1',
    description="Documentation of APIs",
)

# blueprints registration
app.register_blueprint(blog, url_prefix='/blog')

for a in get_config().APPS:
    try:
        import_module(f'{a}.routers')
    except:
        pass


# remove database sessions at the end of the request or when the application shuts down
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
