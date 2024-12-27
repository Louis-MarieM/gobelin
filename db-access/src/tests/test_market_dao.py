from config.tests import db_session
from datetime import datetime
from decimal import Decimal
from sqlalchemy.exc import SQLAlchemyError
from src.daos.asset_dao import AssetDAO
from src.daos.market_dao import MarketDAO
from src.daos.price_dao import PriceDAO
from src.models.asset import Asset
from src.models.market import Market
from src.models.price import Price

def test_get_by_name(db_session):
    """
    Tests markets recovery using partial name match.
    """
    dao = MarketDAO(db_session)

    market1 = Market(name="New York Stock Exchange", region="USA", currency="USD", added_at=datetime(2024, 12, 1))
    market2 = Market(name="Nasdaq", region="USA", currency="USD", added_at=datetime(2024, 12, 1))
    market3 = Market(name="New York other Stock Exchange", region="USA", currency="USD", added_at=datetime(2024, 12, 1))
    dao.create(market1)
    dao.create(market2)
    dao.create(market3)

    matching_markets = dao.get_by_name("New York")
    assert len(matching_markets) == 2
    assert matching_markets[0] == market1
    assert matching_markets[1] == market3

def test_get_by_region(db_session):
    """
    Tests markets recovery in a specific region.
    """
    dao = MarketDAO(db_session)

    market1 = Market(name="Tokyo Stock Exchange", region="Japan", currency="JPY", added_at=datetime(2024, 12, 1))
    market2 = Market(name="New York Stock Exchange", region="USA", currency="USD", added_at=datetime(2024, 12, 1))
    market3 = Market(name="Nasdaq", region="USA", currency="USD", added_at=datetime(2024, 12, 1))
    dao.create(market1)
    dao.create(market2)
    dao.create(market3)

    usa_markets = dao.get_by_region("USA")
    assert len(usa_markets) == 2
    assert all(market.region == "USA" for market in usa_markets)

def test_delete_restrict_by_price(db_session):
    """
    Tests deletion restriction due to foreign key constraint in price data.
    """
    priceDAO = PriceDAO(db_session)
    assetDAO = AssetDAO(db_session)
    marketDAO = MarketDAO(db_session)

    asset = Asset(symbol="AAPL", name="Apple", asset_type="stock", added_at=datetime(2024, 12, 1))
    assetDAO.create(asset)
    market = Market(name="Nasdaq", region="USA", currency="USD", added_at=datetime(2024, 12, 1))
    marketDAO.create(market)
    price = Price(
        asset_id=asset.id,
        market_id=market.id,
        timestamp=datetime(2024, 12, 1),
        interval="1d",
        open_price=Decimal("1.00"),
        close_price=Decimal("1.00"),
        high_price=Decimal("1.00"),
        low_price=Decimal("1.00"),
        volume=Decimal("1000.00")
    )
    priceDAO.create(price)

    try:
        marketDAO.delete(market.id)
        assert False
    except SQLAlchemyError:
        assert marketDAO.get(market.id) is not None

        priceDAO.delete(price.id)
        marketDAO.delete(market.id)
        
        assert priceDAO.get(price.id) is None
        assert marketDAO.get(market.id) is None