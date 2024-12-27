from datetime import datetime
from decimal import Decimal
from config.tests import db_session
from sqlalchemy.exc import SQLAlchemyError
from src.daos.asset_dao import AssetDAO
from src.daos.market_dao import MarketDAO
from src.daos.price_dao import PriceDAO
from src.models.asset import Asset
from src.models.market import Market
from src.models.price import Price

def test_get_by_asset_market_and_period(db_session):
    """
    Tests retrieving prices for a specific asset and market over a period.
    """
    priceDAO = PriceDAO(db_session)
    assetDAO = AssetDAO(db_session)
    marketDAO = MarketDAO(db_session)

    asset1 = Asset(symbol="AAPL", name="Apple", asset_type="stock", added_at=datetime(2024, 12, 1))
    asset2 = Asset(symbol="MSFT", name="Microsoft", asset_type="stock", added_at=datetime(2024, 12, 1))
    assetDAO.create(asset1)
    assetDAO.create(asset2)
    market1 = Market(name="Nasdaq", region="USA", currency="USD", added_at=datetime(2024, 12, 1))
    market2 = Market(name="New York Stock Exchange", region="USA", currency="USD", added_at=datetime(2024, 12, 1))
    marketDAO.create(market1)
    marketDAO.create(market2)

    old_price = Price(
        asset_id=asset1.id,
        market_id=market2.id,
        timestamp=datetime(2024, 12, 1),
        interval="1d",
        open_price=Decimal("100.00"),
        close_price=Decimal("105.00"),
        high_price=Decimal("110.00"),
        low_price=Decimal("95.00"),
        volume=Decimal("1000.00")
    )

    middle_price = Price(
        asset_id=asset1.id,
        market_id=market2.id,
        timestamp=datetime(2024, 12, 2),
        interval="1d",
        open_price=Decimal("100.00"),
        close_price=Decimal("105.00"),
        high_price=Decimal("110.00"),
        low_price=Decimal("95.00"),
        volume=Decimal("1000.00")
    )

    latest_price = Price(
        asset_id=asset1.id,
        market_id=market2.id,
        timestamp=datetime(2024, 12, 3),
        interval="1d",
        open_price=Decimal("100.00"),
        close_price=Decimal("105.00"),
        high_price=Decimal("110.00"),
        low_price=Decimal("95.00"),
        volume=Decimal("1000.00")
    )

    priceDAO.create(old_price)
    priceDAO.create(middle_price)
    priceDAO.create(latest_price)

    fetched_prices = priceDAO.get_by_period(asset1.id, market2.id, datetime(2024, 12, 2), datetime(2024, 12, 4))

    assert len(fetched_prices) == 2
    assert fetched_prices[0] == middle_price
    assert fetched_prices[1] == latest_price

def test_get_latest_price(db_session):
    """
    Tests retrieving the latest price for a specific asset and market.
    """
    priceDAO = PriceDAO(db_session)
    assetDAO = AssetDAO(db_session)
    marketDAO = MarketDAO(db_session)

    asset1 = Asset(symbol="AAPL", name="Apple", asset_type="stock", added_at=datetime(2024, 12, 1))
    asset2 = Asset(symbol="MSFT", name="Microsoft", asset_type="stock", added_at=datetime(2024, 12, 1))
    assetDAO.create(asset1)
    assetDAO.create(asset2)
    market1 = Market(name="Nasdaq", region="USA", currency="USD", added_at=datetime(2024, 12, 1))
    market2 = Market(name="New York Stock Exchange", region="USA", currency="USD", added_at=datetime(2024, 12, 1))
    marketDAO.create(market1)
    marketDAO.create(market2)

    old_AAPL_price = Price(
        asset_id=asset1.id,
        market_id=market1.id,
        timestamp=datetime(2024, 12, 1),
        interval="1d",
        open_price=Decimal("100.00"),
        close_price=Decimal("105.00"),
        high_price=Decimal("110.00"),
        low_price=Decimal("95.00"),
        volume=Decimal("1000.00")
    )

    latest_AAPL_price = Price(
        asset_id=asset1.id,
        market_id=market1.id,
        timestamp=datetime(2024, 12, 2),
        interval="1d",
        open_price=Decimal("100.00"),
        close_price=Decimal("105.00"),
        high_price=Decimal("110.00"),
        low_price=Decimal("95.00"),
        volume=Decimal("1000.00")
    )

    latest_AAPL_bis_price = Price(
        asset_id=asset1.id,
        market_id=market1.id,
        timestamp=datetime(2024, 12, 2),
        interval="2d",
        open_price=Decimal("200.00"),
        close_price=Decimal("205.00"),
        high_price=Decimal("210.00"),
        low_price=Decimal("195.00"),
        volume=Decimal("2000.00")
    )

    latest_AAPL_NY_price = Price(
        asset_id=asset1.id,
        market_id=market2.id,
        timestamp=datetime(2024, 12, 3),
        interval="1d",
        open_price=Decimal("100.00"),
        close_price=Decimal("105.00"),
        high_price=Decimal("110.00"),
        low_price=Decimal("95.00"),
        volume=Decimal("1000.00")
    )

    latest_MSFT_price = Price(
        asset_id=asset2.id,
        market_id=market1.id,
        timestamp=datetime(2024, 12, 3),
        interval="1d",
        open_price=Decimal("100.00"),
        close_price=Decimal("105.00"),
        high_price=Decimal("110.00"),
        low_price=Decimal("95.00"),
        volume=Decimal("1000.00")
    )

    priceDAO.create(old_AAPL_price)
    priceDAO.create(latest_AAPL_price)
    priceDAO.create(latest_AAPL_bis_price)
    priceDAO.create(latest_AAPL_NY_price)
    priceDAO.create(latest_MSFT_price)
    
    fetched_price = priceDAO.get_latest_price(asset1.id, market1.id)

    assert fetched_price == latest_AAPL_price

def test_get_price_stats(db_session):
    """
    Tests retrieving price statistics (average, max, min) for an asset in a specific market over a period.
    """
    priceDAO = PriceDAO(db_session)
    assetDAO = AssetDAO(db_session)
    marketDAO = MarketDAO(db_session)

    asset1 = Asset(symbol="AAPL", name="Apple", asset_type="stock", added_at=datetime(2024, 12, 1))
    asset2 = Asset(symbol="MSFT", name="Microsoft", asset_type="stock", added_at=datetime(2024, 12, 1))
    assetDAO.create(asset1)
    assetDAO.create(asset2)
    market1 = Market(name="Nasdaq", region="USA", currency="USD", added_at=datetime(2024, 12, 1))
    market2 = Market(name="New York Stock Exchange", region="USA", currency="USD", added_at=datetime(2024, 12, 1))
    marketDAO.create(market1)
    marketDAO.create(market2)

    old_price = Price(
        asset_id=asset1.id,
        market_id=market2.id,
        timestamp=datetime(2024, 12, 1),
        interval="1d",
        open_price=Decimal("1.00"),
        close_price=Decimal("1.00"),
        high_price=Decimal("1.00"),
        low_price=Decimal("1.00"),
        volume=Decimal("1000.00")
    )

    middle_price = Price(
        asset_id=asset1.id,
        market_id=market2.id,
        timestamp=datetime(2024, 12, 2),
        interval="1d",
        open_price=Decimal("100.00"),
        close_price=Decimal("100.00"),
        high_price=Decimal("110.00"),
        low_price=Decimal("90.01"),
        volume=Decimal("1000.00")
    )

    latest_price = Price(
        asset_id=asset1.id,
        market_id=market2.id,
        timestamp=datetime(2024, 12, 3),
        interval="1d",
        open_price=Decimal("100.00"),
        close_price=Decimal("105.00"),
        high_price=Decimal("115.00"),
        low_price=Decimal("95.00"),
        volume=Decimal("1000.00")
    )

    priceDAO.create(old_price)
    priceDAO.create(middle_price)
    priceDAO.create(latest_price)

    stats = priceDAO.get_price_stats(asset1.id, market2.id, datetime(2024, 12, 2), datetime(2024, 12, 3))

    assert stats["average_price"] == Decimal("102.5")
    assert stats["max_price"] == Decimal("115.0")
    assert stats["min_price"] == Decimal("90.01")

def test_create_error_asset_not_exist(db_session):
    """
    Tests creation error due to incorrect asset foreign key.
    """
    priceDAO = PriceDAO(db_session)
    assetDAO = AssetDAO(db_session)
    marketDAO = MarketDAO(db_session)

    asset = Asset(symbol="AAPL", name="Apple", asset_type="stock", added_at=datetime(2024, 12, 1))
    assetDAO.create(asset)
    market = Market(name="Nasdaq", region="USA", currency="USD", added_at=datetime(2024, 12, 1))
    marketDAO.create(market)

    invalid_price = Price(
        asset_id=asset.id + 1,
        market_id=market.id,
        timestamp=datetime(2024, 12, 1),
        interval="1d",
        open_price=Decimal("1.00"),
        close_price=Decimal("1.00"),
        high_price=Decimal("1.00"),
        low_price=Decimal("1.00"),
        volume=Decimal("1000.00")
    )

    valid_price = Price(
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
    
    try:
        priceDAO.create(invalid_price)
        assert False
    except SQLAlchemyError:
        assert len(priceDAO.get_all()) == 0

        new_price = priceDAO.create(valid_price)
        
        assert priceDAO.get(new_price.id) == valid_price

def test_create_error_market_not_exist(db_session):
    """
    Tests creation error due to incorrect market foreign key.
    """
    priceDAO = PriceDAO(db_session)
    assetDAO = AssetDAO(db_session)
    marketDAO = MarketDAO(db_session)

    asset = Asset(symbol="AAPL", name="Apple", asset_type="stock", added_at=datetime(2024, 12, 1))
    assetDAO.create(asset)
    market = Market(name="Nasdaq", region="USA", currency="USD", added_at=datetime(2024, 12, 1))
    marketDAO.create(market)

    invalid_price = Price(
        asset_id=asset.id,
        market_id=market.id + 1,
        timestamp=datetime(2024, 12, 1),
        interval="1d",
        open_price=Decimal("1.00"),
        close_price=Decimal("1.00"),
        high_price=Decimal("1.00"),
        low_price=Decimal("1.00"),
        volume=Decimal("1000.00")
    )

    valid_price = Price(
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
    
    try:
        priceDAO.create(invalid_price)
        assert False
    except SQLAlchemyError:
        assert len(priceDAO.get_all()) == 0

        new_price = priceDAO.create(valid_price)
        
        assert priceDAO.get(new_price.id) == valid_price
