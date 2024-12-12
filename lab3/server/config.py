import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:pass@localhost:5432/webapp'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
