---
tags:
  - flask
  - programming-language
  - python
---
# Flask

Quick & dirty collection of thoughts on using the Flask web framework for
backend development with python.

## Flask: Extensions

Flask extensions are plugins which provide additional functionality for your web
application. Extensions need to be initialized and added to your flask app as shown
below.

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask("__name__", static_folder=None)
db = SQLAlchemy()

db.init_app(app)
```

### Flask-Restful

Flask-restful provides classes to quickly slap together web APIs which work with
your existing ORM while also trying to encourage best practices of Restful services.

#### Flask-Restful: Basic usage

Heres a super basic example from their docs...

```python
# my_project/app.py
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {"hello": "world"}

api.add_resource(HelloWorld, "/")

if __name__ == "__main__":
    app.run(debug=True)
```

In this example the `HellowWorld` class is what will be called when a request is
made to the endpoint `/` each method of this class maps to the respective method
of the REST request they are responsible for. For most resources you'd be looking
to add methods like:

* `get()`
* `post()`
* `put()`
* `delete()`

#### Flask-Restful: Accepting arguments

Here is an example of a resource which will accept `node_id` as an argument...

```python
# my_project/app.py
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class User(Resource):
    def get(self, user_id):
        return {"received": user_id}

api.add_resource(User, "/users/<int:user_id>", endpoint="user")
```

This is similar to flask's out-of-the-box support for routing arguments
with the `route` decorator. The above `api.add_resource...` line is
equivalent to using `@app.route("/users/<user_id>")`.

Much like when using the decorator, the argument extracted from the request
URL will be given to the appropriate method as an argument (note the `get` method
expecting a `user_id` to be passed).

You can do this with an arbitrary number of arguments or leverage the
`marshal_with` decorator which I will not be covering.

#### Flask-Restful: Using Blueprints

My preferred way to use `flask-restful` is to add my resources to blueprints
to be registered with my `app`.

Heres an example of how to do that...

```python
# my_project/user/views.py
from flask import Blueprint
from flask_restful import Api, Resource

bp = Blueprint("users", __name__)
api = Api(bp)


class Users(Resource):
    def get(self, user_id):
        return {"received": user_id}


api.add_resource(Users, "/users/<int:user_id>", endpoint="user")
# my_project/app.py
from flask import Flask
from my_project.user.views import bp as user_blueprint


app = Flask(__name__)
url_prefix = "/api/v1"
app.register_blueprint(user_blueprint, url_prefix=url_prefix)
app.run()
```

#### Flask-Restful: Field validation

Flask-restful also has a few objects which can be used in concert with
the `@marshal_with` decorator to validate the body of a given request,
but I prefer to use [marshmallow](https://marshmallow.readthedocs.io/en/stable/)
for that, so I won't be going into any detail here. Refer to the docs for more info.

#### Flask-Restful: Further reading

[Flask-Restful Docs](https://flask-restful.readthedocs.io/en/latest/)

### Flask-SQLAlchemy

Since `flask-sqlalchemy` is basically just a wrapper to combine Flask and SQLAlchemy
much of this is not Flask specific and could be leveraged with straight SQLAlchemy.

#### Flask-SQLAlchemy: Further reading

[My SQLAlchemy notes](sqlalchemy.md)
[Flask-SQLAlchemy Docs](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
[SQLAlchemy Docs](https://docs.sqlalchemy.org/en/13/)

### Flask-Migrate

TODO

## Flask: Application Factory

The application factory pattern is the recommended way to structure a Flask application. Instead of creating a global `app` object, you create it inside a function, `create_app`. This approach has several advantages:

*   **Improved Testing**: You can create multiple instances of your application with different configurations for testing.
*   **Avoiding Circular Imports**: It helps manage dependencies and avoids circular import problems with extensions and blueprints.
*   **Scalability**: It makes the application more modular and easier to scale.

Here is an example of a `create_app` function that ties together the configuration, extensions, and blueprints.

```python
# my_project/app.py
from flask import Flask
from my_project.config import MyAppConfig
from my_project.database import db
from my_project.user.views import bp as user_blueprint

def create_app(config_object=MyAppConfig()):
    """An application factory, as described in the Flask documentation."""
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    url_prefix = "/api/v1"
    app.register_blueprint(user_blueprint, url_prefix=url_prefix)

    return app
```

This `create_app` function can then be used by your test suite (as shown in the testing section) or by a WSGI server to run your application.

## Flask: Testing

Flask apps have a built-in Werkzeug test client which can be used within unit tests.
The below `pytest` example will...

* Initialize our App using a config object
* Provision a fresh database instance and provide a valid session
* return a test client to use within unit tests

```python
# my_project/tests/conftest.py
import pytest

from my_project.app import create_app
from my_project.config import MyAppConfig
from my_project.database import db as app_db


@pytest.fixture(scope="session")
def app(request):
    flask_app = create_app(MyAppConfig())
    with flask_app.app_context():
        yield flask_app


@pytest.fixture(scope="session")
def db(app, request):
    app_db.drop_all()
    app_db.create_all()
    yield app_db
    app_db.drop_all()


@pytest.fixture(scope="function")
def session(db, request):
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    sess = db.create_scoped_session(options=options)

    db.session = sess
    yield sess

    sess.remove()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(app, session):
    with app.test_client() as c:
        yield c


# my_project/tests/test_user_endpoint.py
def test_users_get(client):
    response = client.get("/api/v1/users")

    assert response.status_code == 200
```

### Flask Testing: Further reading

[Testing Flask Applications](https://flask.palletsprojects.com/en/1.1.x/testing/)

### Marshmallow

TODO
