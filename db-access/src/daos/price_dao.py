from datetime import datetime
from sqlalchemy.sql import func
from src.daos.base_dao import BaseDAO
from src.models.price import Price

class PriceDAO(BaseDAO):
    def __init__(self, db):
        super().__init__(Price, db)

    def get_by_period(self, asset_id: int, market_id: int, start_date: datetime, end_date: datetime):
        return self.db.query(self.model).filter(
            self.model.asset_id == asset_id,
            self.model.market_id == market_id,
            self.model.timestamp >= start_date,
            self.model.timestamp <= end_date
        ).all()

    def get_latest_price(self, asset_id: int, market_id: int):
        """
        Returns price with latest timestamp.
        """
        return self.db.query(self.model).filter(
            self.model.asset_id == asset_id,
            self.model.market_id == market_id
        ).order_by(self.model.timestamp.desc()).first()

    def get_price_stats(self, asset_id: int, market_id: int, start_date: datetime, end_date: datetime):
        """
        Returns a Dictionnary with following attributes :
            - average_price : average of close prices over a period.
            - max_price : max price on period.
            - min_price : min price on period.
        """
        stats = self.db.query(
            func.avg(self.model.close_price).label("average_price"),
            func.max(self.model.high_price).label("max_price"),
            func.min(self.model.low_price).label("min_price")
        ).filter(
            self.model.asset_id == asset_id,
            self.model.market_id == market_id,
            self.model.timestamp >= start_date,
            self.model.timestamp <= end_date
        ).one()

        return {
        "average_price": stats[0],
        "max_price": stats[1],
        "min_price": stats[2]
    }
