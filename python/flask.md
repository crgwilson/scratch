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

class HellowWorld(Resource):
    def get(self):
      return {"hello": "world"}

api.add_resource(HellowWorld, "/")

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

api.add_resource(Users, "/users/<int:user_id>, endpoint="user")
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


class Users(resource):
    def get(self, node_id):
        return {"received": user_id}


api.add_resource(Users, "/users/<int:user_id>, endpoint="user")
# my_project/app.py
from flask import Flask
from my_project.users import bp as user_blueprint


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

## Flask: Testing

Flask apps have a built-in Werkzeug test client which can be used within unit tests.
The below `pytest` example will...

* Initialize our App using a config object
* Provision a fresh database instance and provide a valid session
* return a test client to use within unit tests

```python
# myproject/tests/conftest.py
import pytest

from my_project.app import create_app
from my_project.config import MyAppConfig
from my_app.database import db as app_db


@pytest.yield_fixture(scope="session")
def app(request):
    flask_app = create_app(MyAppConfig())
    ctx = flask_app.app_context()
    ctx.push()

    yield flask_app

    ctx.pop()


@pytest.fixture(scope="session")
def db(app, request):
    app_db.drop_all()
    app_db.create_all()

    app_db.app = app
    yield app_db

    app_db.drop_all()


@pytest.yield_fixture(scope="function")
def session(db, request):
    db.session.begin_nested()
    yield db.session
    db.session.rollback()


@pytest.fixture(scope="function")
def client(app, session):
    with app.test_client() as c:
        yield c


# myproject/tests/test_user_endpoint.py
def test_users_get(client):
    response = client.get("/api/v1/users")

    assert response.status_code == 200
```

### Flask Testing: Further reading

[Testing Flask Applications](https://flask.palletsprojects.com/en/1.1.x/testing/)

### Marshmallow

TODO
