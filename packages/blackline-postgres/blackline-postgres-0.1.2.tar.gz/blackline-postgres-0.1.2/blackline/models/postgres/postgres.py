"""
Postgres adapter configuration. This shouldn't be here but will move is
later and have it dynamically loaded from blackline-postgres.
"""

from typing import Literal

from blackline.models.datastore_base import ConnectionConfig, DataStoreBase
from pydantic import BaseModel, SecretStr


class PostgresConnInfo(BaseModel):
    host: str
    port: int
    dbname: str
    user: str
    password: SecretStr


class PostgresConnectionConfig(ConnectionConfig):
    conninfo: PostgresConnInfo


class PostgresDataStore(DataStoreBase):
    class Config(BaseModel):
        connection: PostgresConnectionConfig

    type: Literal["postgres"]
    config: Config
