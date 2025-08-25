# data_access.py
from sqlalchemy import create_engine, text
import pandas as pd

# ===============================
# DATABASE CONFIGURATION
# ===============================
DB_URL = "mysql+mysqlconnector://root:123456789@localhost/retail_optimizer"

# Create SQLAlchemy engine
engine = create_engine(DB_URL, echo=False)

# ===============================
# HELPER FUNCTIONS
# ===============================
def fetch_query(sql: str, params=None) -> pd.DataFrame:
    """
    Execute a SELECT query and return results as DataFrame.
    """
    with engine.connect() as conn:
        result = pd.read_sql(sql=text(sql), con=conn, params=params)
    return result

def execute_query(sql: str, params=None):
    """
    Execute INSERT/UPDATE/DELETE query.
    """
    with engine.connect() as conn:
        conn.execute(text(sql), params or {})
        conn.commit()
