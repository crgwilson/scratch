# SQLAlchemy

Notes regarding the `SQLAlchemy` python library

## Usage

### Queries

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

## Inserting reference data

If you have a need to insert a few static records into a table one-time during
initialization, you can do so with the `sqlalchemy.event.listen` function.

```python
from sqlalchemy.event import listen

from myapp.database import db


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)

    profile_name = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)


def insert_default_users(*args, **kwargs):
    db.session.add(User(id=1, profile_name="admin", first_name="Systems", last_name="Administrator"))
    db.session.commit()


listen(User.__table__, "after_create", insert_default_users)
```

## Further reading

* [SQLAlchemy Docs](https://docs.sqlalchemy.org/en/13/)
