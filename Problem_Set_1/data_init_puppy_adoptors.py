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
    i = 1
    while (i < 9):
        print i
        print puppies_list[i]
        puppy_adopt = PuppyAdoptors(id=None, puppy_id=puppies_list[i].id,
                                    adoptor_id=randint(1, 8))
        session.add(puppy_adopt)
        session.commit()
        i += 1
except:
    session.rollback()
    raise
