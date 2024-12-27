from src.daos.base_dao import BaseDAO
from src.models.market import Market

class MarketDAO(BaseDAO):
    def __init__(self, db):
        super().__init__(Market, db)

    def get_by_name(self, name: str):
        return self.db.query(self.model).filter(self.model.name.ilike(f"%{name}%")).all()

    def get_by_region(self, region: str):
        return self.db.query(self.model).filter(self.model.region == region).all()
