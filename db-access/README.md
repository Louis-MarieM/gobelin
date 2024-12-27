# Db-access - ORM module
DAO layer to manage database connection pool and requests to database.
Compiled as a package and usable by others modules.

## Config
#### Orm
[`orm.py`](/db-access/config/orm.py) configures connection pool and session factory from SQLAlchemy.
It allows also ORM models definition with Base class.
#### Package
Package configuration upcoming soon...
#### Tests
[`tests.py`](/db-access/config/tests.py) override [`orm.py`](/db-access/config/orm.py) configuration for tests and create a test model. 
It provides a sqlite database session using pytest fixtures and SQLAlchemy events, so each test has an new blank database.

## Models
Each model corresponds to a database table defined in [migration folder](/db/migrations/).

## Daos
[`session.py`](/db-access/src/daos/session.py) gives session getter to use in the others modules of the project. 
Basic CRUD methods are define in [`base_dao.py`](/db-access/src/daos/base_dao.py). Others DAO files define specific methods for each model. [`session.py`](/db-access/src/daos/session.py) gives session getter to use in 

## Tests
Covers the session getter and all daos method except some model getters.
