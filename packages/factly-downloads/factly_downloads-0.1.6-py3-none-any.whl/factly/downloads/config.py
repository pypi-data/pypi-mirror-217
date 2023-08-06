import logging

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    S3_ACCESS_KEY: str = ""
    S3_SECRET_KEY: str = ""
    S3_HOST: str = "https://s3.ap-southeast-1.wasabisys.com"
    S3_REGION: str = "ap-southeast-1"

    @validator("*", pre=True)
    def check_fields(cls, value):
        if not value:
            raise ValueError("Environment Variable are not set properly")
        return value

    @validator("S3_HOST")
    def validate_gender(cls, value):
        if "ap-southeast-1" not in value:
            logging.warning(
                "Deprecated region {wasabi_host_url}, please use / setup `ap-southeast-1"
            )
        return value

    class Config:
        env_file = ".env"
