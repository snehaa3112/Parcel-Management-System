import os

class Config:
    SECRET_KEY = 'f9dc74e302dd410511b72d8e25350cbb56ce1a84026798ee'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/parcel_management'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
