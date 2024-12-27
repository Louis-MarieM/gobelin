from sqlalchemy import text
from src.daos.session import get_db

def test_database_connection():
    """
    Tests if database connection configuration is valid.
    """
    try:
        session = next(get_db())
        result = session.execute(text("SELECT 1"))
        assert result.scalar() == 1, "Database connection failed"
    except Exception as e:
        assert False, f"Database connection failed: {e}"