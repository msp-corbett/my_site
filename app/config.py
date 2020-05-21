""" App Configuration """
from os import environ
from typing import List, Type


class BaseConfig:
    CONFIG_NAME = "base"
    USE_MOCK_EQUIVALENCY = False
    DEBUG = False
    TRAP_HTTP_EXCEPTIONS = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_CHECK_DEFAULT = False


class DevelopmentConfig(BaseConfig):
    CONFIG_NAME = "development"
    SECRET_KEY = environ.get('DEV_SECRET_KEY', 'TheyTried2MakeMeG02Rhab')
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{environ.get('DB_PATH')}\\app-dev.db"
    WTF_CSRF_SECRET_KEY = environ.get("WTF_SECRET_KEY", "But1SaidN0NoN0!")


class TestingConfig(BaseConfig):
    CONFIG_NAME = "test"
    SECRET_KEY = environ.get("TEST_SECRET_KEY", "KingJeremyTheWicked")
    DEBUG = False
    TESTING = True
    LOGIN_DISABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI =  f"sqlite:///{environ.get('DB_PATH')}\\app-test.db"
    WTF_CSRF_SECRET_KEY = environ.get("WTF_SECRET_KEY", "WeUnleashedAl10n")


class ProductionConfig(BaseConfig):
    CONFIG_NAME = "production"
    SECRET_KEY = environ.get("PROD_SECRET_KEY", "BikiniBott0m5LagerT0p5")
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI =  f"sqlite:///{environ.get('DB_PATH')}\\app-prod.db"
    WTF_CSRF_SECRET_KEY = environ.get("WTF_SECRET_KEY", "T1meFlysByInTheYe110w&Green")


EXPORT_CONFIGS: List[Type[BaseConfig]] = [
    DevelopmentConfig,
    TestingConfig,
    ProductionConfig,
]

config_by_name = {cfg.CONFIG_NAME: cfg for cfg in EXPORT_CONFIGS}
