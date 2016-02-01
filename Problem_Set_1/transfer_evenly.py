import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import decimal as import_decimal
from decimal import Decimal

Base = declarative_base()

from puppies import Shelter, Base, Puppy

import datetime as import_datetime
from datetime import date
from datetime import datetime

engine = create_engine('sqlite:///puppyshelter.db')

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine


DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

try:
# get all puppies
session.query(User).filter(User.name.like('%ed')).count()
# get all shelters

# devide puppies by shelter
# round the number
# update puppy_shelter table to update puppy assignments

except:
   session.rollback()
   raise

