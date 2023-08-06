from typing import List
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    """
    settings for connecting to MongoDB. Use environment variables or a `.env` file to set these settings

    Example:
        To set the `mongodb_uri`::

            $ MONGODB_URI=<connection_string>
    """
    mongodb_uri: str
    """URI to connect to the mongo instance(s). This is required."""
    mongodb_database_name: str = "default"
    """Name of the database to target"""


    @classmethod
    @validator("mongodb_uri")
    def check_not_empty(cls, v):
        assert v != "", f"{v} is not defined"
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()



