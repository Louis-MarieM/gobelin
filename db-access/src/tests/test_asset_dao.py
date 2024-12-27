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

def test_get_by_symbol(db_session):
    """
    Tests recovery of an asset by a symbol match.
    """
    dao = AssetDAO(db_session)

    asset1 = Asset(symbol="AAPL", name="Apple", asset_type="stock", added_at=datetime(2024, 12, 1))
    asset2 = Asset(symbol="MSFT", name="Microsoft", asset_type="stock", added_at=datetime(2024, 12, 1))
    dao.create(asset1)
    dao.create(asset2)

    matching_asset = dao.get_by_symbol("AAPL")
    assert matching_asset == asset1

def test_get_by_type(db_session):
    """
    Tests recovery of all assets of a specific type.
    """
    dao = AssetDAO(db_session)

    asset1 = Asset(symbol="AAPL", name="Apple", asset_type="stock", added_at=datetime(2024, 12, 1))
    asset2 = Asset(symbol="MSFT", name="Microsoft", asset_type="stock", added_at=datetime(2024, 12, 1))
    asset3 = Asset(symbol="BTC", name="Bitcoin", asset_type="crypto", added_at=datetime(2024, 12, 1))
    dao.create(asset1)
    dao.create(asset2)
    dao.create(asset3)

    matching_assets = dao.get_by_type("stock")
    assert len(matching_assets) == 2
    assert matching_assets[0] == asset1
    assert matching_assets[1] == asset2

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
        assetDAO.delete(asset.id)
        assert False
    except SQLAlchemyError:
        assert assetDAO.get(asset.id) is not None

        priceDAO.delete(price.id)
        assetDAO.delete(asset.id)

        assert priceDAO.get(price.id) is None
        assert assetDAO.get(asset.id) is None