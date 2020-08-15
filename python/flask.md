# Flask

Quick & dirty collection of thoughts on using the Flask web framework for
backend development with python.

## Extensions

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

### Flask-SQLAlchemy

Since `flask-sqlalchemy` is basically just a wrapper to combine Flask and SQLAlchemy
much of this is not Flask specific and could be leveraged with straight SQLAlchemy.

[Flask-SQLAlchemy Docs](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
[SQLAlchemy Docs](https://docs.sqlalchemy.org/en/13/)

#### Models

TODO

#### Queries

Basic SQL queries are pretty easy to put together with SQLAlchemy. You can get a
query object from your current DB session and filter that as necessary.

This super simple example query...

```sql
SELECT * FROM users WHERE id = '10';
```

...would translate to...

```python
from myapp.extensions import db  # db = flask_sqlalchemy.SQLAlchemy()
from myapp.users.models import UserModel

db.session.query(UserModel).filter(UserModel.id == 10).first()
```

...and this query...

```sql
SELECT id FROM users WHERE name LIKE "%bob&";
```

...would be...

```python
from myapp.extensions import db  # db = flask_sqlalchemy.SQLAlchemy()
from myapp.users.models import UserModel

db.session.query(UserModel.id).filter(UserModel.id.like("%bob%")).all()
```

We can do something a little more complicated too. Here is an example
using a nested query...

```sql
SELECT
  *
FROM
  child
WHERE
  name = 'bob junior'
AND
  parent_id=(SELECT id FROM parent WHERE name='bob');
```

...would be...

```python
from sqlalchemy import and_

from myapp.extensions import db  # db = flask_sqlalchemy.SQLAlchemy()
from myapp.parents.models import ParentModel
from myapp.children.models import ChildModel

session = db.session

sub_query = session.query(ParentModel.id).filter(ParentModel.name == "bob").subquery()
query = session.query(ChildModel).filter(
  and_(
    ChildModel.name == "bob junior",
    ChildModel.parent_id.in_(sub_query)
  )
)
```

...note that we're using the `sqlalchemy.and_` function here to match the `AND`
keyword in regular SQL. If we wanted to do an `OR` instead we could use the
(hopefully obvious) `sqlalchemy.or_` function instead.
