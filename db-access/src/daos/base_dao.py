from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class BaseDAO:
    """
    A generic DAO (Data Access Object) class to perform CRUD operations on a database table.
    """
    def __init__(self, model, db: Session):
        self.model = model
        self.db = db

    def get(self, id: int):
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self):
        return self.db.query(self.model).all()

    def create(self, obj):
        """
        Creates a new data with given model.
        If the creation succeeds, returns the new data.
        """
        try:
            self.db.add(obj)
            self.db.commit()
            self.db.refresh(obj)
            return obj
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def delete(self, id: int):
        """
        Deletes the data with the given id parameter.
        If the deletion succeeds, returns the latest version of the data.
        """
        try:
            obj = self.get(id)
            if obj:
                self.db.delete(obj)
                self.db.commit()
            return obj
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def update(self, id: int, updates: dict):
        """
        Updates the data with the given id parameter.
        If the update succeeds, return the new version od the data.
        """
        try:
            obj = self.get(id)
            if obj:
                for key, value in updates.items():
                    setattr(obj, key, value)
                self.db.commit()
                self.db.refresh(obj)
            return obj
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
