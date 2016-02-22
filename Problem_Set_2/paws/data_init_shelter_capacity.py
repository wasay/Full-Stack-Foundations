from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, engine, Shelters
# from flask.ext.sqlalchemy import SQLAlchemy

from random import randint
import random

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

try:

    for row in session.query(Shelters.id).\
                       order_by(Shelters.name):
        session.query(Shelters.id).\
                filter(Shelters.id == row.id).\
                update({'current_occupancy': 0,
                        'maximum_capacity': randint(0, 10)})
        session.commit()
except:
    session.rollback()
    raise
