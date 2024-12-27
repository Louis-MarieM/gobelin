import pytest
from src.daos.base_dao import BaseDAO
from config.tests import TestModel, db_session
from sqlalchemy.exc import SQLAlchemyError

def test_create_and_get(db_session):
    """
    Tests creating an instance and retrieving it by its ID successfully.
    """
    dao: BaseDAO[TestModel] = BaseDAO(TestModel, db_session)

    # Create test
    new_row: TestModel = TestModel(name="Test name")
    dao.create(new_row)
    assert new_row.id is not None
    assert new_row.name == "Test name"

    # Get test
    fetched_row: TestModel = dao.get(new_row.id)
    assert fetched_row == new_row

def test_create_with_error(db_session):
    """
    Tests error handling during the creation of an invalid instance and rollbacking successfully.
    """
    dao: BaseDAO[TestModel] = BaseDAO(TestModel, db_session)
    new_row: TestModel = TestModel(name=None)

    try:
        dao.create(new_row)
        assert False
    except SQLAlchemyError:
        fetched_row = dao.get(new_row.id)
        assert fetched_row is None

def test_update_and_delete(db_session):
    """
    Tests updating and deleting an instance successfully.
    """
    dao: BaseDAO[TestModel] = BaseDAO(TestModel, db_session)

    # Creation of a new row
    new_row: TestModel = TestModel(name="To Update")
    dao.create(new_row)

    # Update test
    updates: dict = {"name": "Updated row"}
    updated_row: TestModel = dao.update(new_row.id, updates)
    assert updated_row.name == "Updated row"

    # Delete test
    deleted_row: TestModel = dao.delete(new_row.id)
    assert deleted_row.id == new_row.id
    assert dao.get(new_row.id) is None

def test_update_with_error(db_session):
    """
    Tests error handling during an update with invalid data and rollbacking successfully.
    """
    dao: BaseDAO[TestModel] = BaseDAO(TestModel, db_session)
    new_row: TestModel = TestModel(name="Valid name")
    dao.create(new_row)

    try:
        invalid_updates: dict = {"name": None}
        dao.update(new_row.id, invalid_updates)
        assert False
    except SQLAlchemyError:
        fetched_row: TestModel = dao.get(new_row.id)
        assert fetched_row.name == "Valid name"

def test_delete_with_error(mocker, db_session):
    """
    Tests error handling during the deletion of an instance and rollbacking successfully.
    """
    dao: BaseDAO[TestModel] = BaseDAO(TestModel, db_session)
    new_row: TestModel = TestModel(name="Test name")
    dao.create(new_row)

    mock_delete = mocker.patch.object(db_session, "delete", side_effect=SQLAlchemyError("Simulated delete error"))

    with pytest.raises(SQLAlchemyError) as error:
        dao.delete(new_row.id)

    mock_delete.assert_called_once_with(new_row)
    assert str(error.value) == "Simulated delete error"
    assert dao.get(new_row.id) is not None

def test_get_all(db_session):
    """
    Tests retrieving all instances successfully.
    """
    dao: BaseDAO[TestModel] = BaseDAO(TestModel, db_session)
    first_row: TestModel = TestModel(name="First row")
    second_row: TestModel = TestModel(name="Second row")
    dao.create(first_row)
    dao.create(second_row)

    created_rows = dao.get_all()

    assert len(created_rows) == 2
    assert created_rows[0].name == first_row.name
    assert created_rows[1].name == second_row.name
