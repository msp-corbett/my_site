""" App Configuration """
from os import environ, path
from typing import List, Type


class BaseConfig:
    CONFIG_NAME = "base"
    USE_MOCK_EQUIVALENCY = False
    DEBUG = False
    TRAP_HTTP_EXCEPTIONS = True


class DevelopmentConfig(BaseConfig):
    CONFIG_NAME = "development"
    SECRET_KEY = environ.get('DEV_SECRET_KEY', 'TheyTried2MakeMeG02Rhab')
    TESTING = False
    

class TestingConfig(BaseConfig):
    CONFIG_NAME = "test"
    SECRET_KEY = environ.get("TEST_SECRET_KEY", "KingJeremyTheWicked")
    DEBUG = False
    TESTING = True
    LOGIN_DISABLED = True


class ProductionConfig(BaseConfig):
    CONFIG_NAME = "production"
    SECRET_KEY = environ.get("PROD_SECRET_KEY", "BikiniBott0m5LagerT0p5")
    DEBUG = False
    TESTING = False


EXPORT_CONFIGS: List[Type[BaseConfig]] = [
    DevelopmentConfig,
    TestingConfig,
    ProductionConfig,
]

config_by_name = {cfg.CONFIG_NAME: cfg for cfg in EXPORT_CONFIGS}
