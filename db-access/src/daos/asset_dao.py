from src.daos.base_dao import BaseDAO
from src.models.asset import Asset

class AssetDAO(BaseDAO):
    def __init__(self, db):
        super().__init__(Asset, db)

    def get_by_symbol(self, symbol: str):
        return self.db.query(self.model).filter(self.model.symbol == symbol).first()

    def get_by_type(self, asset_type: str):
        return self.db.query(self.model).filter(self.model.asset_type == asset_type).all()
