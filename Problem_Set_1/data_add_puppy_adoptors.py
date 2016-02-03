from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from puppies import Shelter, Base, Puppy, PuppyAdoptors, engine
# from flask.ext.sqlalchemy import SQLAlchemy

from random import randint
import random

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

try:
    puppies_list = session.query(Puppy.id, Puppy.name).order_by(Puppy.name)
    for i, row in enumerate(puppies_list):
        print i
        print row
        puppy_adopt = PuppyAdoptors(id=None, puppy_id=row.id, adoptor_id=randint(0, 8))
        session.add(puppy_adopt)
        session.commit()
except:
   session.rollback()
   raise
