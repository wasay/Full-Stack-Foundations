from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from puppies import Shelter, Base, Puppy, engine
# from flask.ext.sqlalchemy import SQLAlchemy

from random import randint
import random

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

try:

    for row in session.query(Shelter.id).\
                       order_by(Shelter.name):
        session.query(Shelter.id).\
                filter(Shelter.id == row.id).\
                update({'current_occupancy' : 0,
                        'maximum_capacity' : randint(0, 10)})
        session.commit()
except:
   session.rollback()
   raise
