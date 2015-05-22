from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import *

# an Engine, which the Session will use for connection
# resources
some_engine = create_engine(DATABASE_URL)

# create a configured "Session" class
Session = sessionmaker(bind=some_engine)

