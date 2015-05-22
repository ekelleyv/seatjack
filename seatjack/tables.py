from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, backref
from sqlalchemy.dialects.mysql.base import TINYINT, BIGINT
from sqlalchemy.schema import CreateTable

import datetime
import json

DeclarativeBase = declarative_base()

class ImageTweet(DeclarativeBase):
    __tablename__ = "image_tweets"

    id = Column(u'id', INTEGER(), primary_key=True, nullable=False, autoincrement=True)
    tweet_id = Column(u'tweet_id', BIGINT(), nullable=False)
    original_image_url = Column(u'original_image_url', VARCHAR(255), nullable=False)
    tweet_body = Column(u'tweet_body', VARCHAR(255), nullable=False)
    image_key = Column(u'image_key', VARCHAR(255), nullable=True)
    barcode_value = Column(u'barcode_value', VARCHAR(255), nullable=True)
    parsed = Column(INT(), default=0)
    created_at = Column(DATETIME(timezone=False), nullable=False, default=datetime.datetime.utcnow)
    updated_at = Column(DATETIME(timezone=False), nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


if __name__ == '__main__':
    print CreateTable(ImageTweet.__table__)
