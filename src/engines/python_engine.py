import os
import pandas as pd
from abc import ABC, abstractmethod
from sqlalchemy import create_engine
from snowflake.connector import connect
from snowflake.connector.pandas_tools import write_pandas

class BaseEngine(ABC):
    """Abstract Base Class for all Data Engines"""
    @abstractmethod
    def read(self, query: str) -> pd.DataFrame:
        pass

    @abstractmethod
    def write(self, df: pd.DataFrame, table_name: str):
        pass

    @abstractmethod
    def transform(self, sql: str):
        pass

class SnowflakeEngine(BaseEngine):
    def __init__(self):
        # Connection params from environment variables
        self.user = os.getenv('SNOWFLAKE_USER')
        self.password = os.getenv('SNOWFLAKE_PASSWORD')
        self.account = os.getenv('SNOWFLAKE_ACCOUNT')
        self.database = os.getenv('SNOWFLAKE_DATABASE')
        self.schema = os.getenv('SNOWFLAKE_SCHEMA')
        self.warehouse = os.getenv('SNOWFLAKE_WAREHOUSE')
        self.role = os.getenv('SNOWFLAKE_ROLE')

        # SQLAlchemy Engine for SQL execution and metadata
        self.conn_url = (
            f"snowflake://{self.user}:{self.password}@{self.account}/"
            f"{self.database}/{self.schema}?warehouse={self.warehouse}&role={self.role}"
        )
        self.sql_engine = create_engine(self.conn_url)

    def read(self, query: str) -> pd.DataFrame:
        """Reads Snowflake data into a Pandas DataFrame"""
        print(f"Reading data from Snowflake via query: {query[:50]}...")
        return pd.read_sql(query, self.sql_engine)

    def transform(self, sql: str):
        """Executes SQL transformations directly on Snowflake (Push-down)"""
        print("Executing Snowflake SQL transformation...")
        with self.sql_engine.connect() as conn:
            conn.execute(sql)

    def write(self, df: pd.DataFrame, table_name: str):
        """High-performance write back to Snowflake"""
        print(f"Writing {len(df)} rows to Snowflake table: {table_name}")
        ctx = connect(
            user=self.user, password=self.password, account=self.account,
            warehouse=self.warehouse, database=self.database,
            schema=self.schema, role=self.role
        )
        try:
            write_pandas(ctx, df, table_name.upper(), auto_create_table=True)
        finally:
            ctx.close()

class EngineFactory:
    """Factory to instantiate the correct engine based on configuration"""
    @staticmethod
    def get_engine(mode: str) -> BaseEngine:
        if mode.lower() == "snowflake":
            return SnowflakeEngine()
        # elif mode.lower() == "spark": return SparkEngine()
        raise ValueError(f"Engine mode '{mode}' is not supported yet.")