import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from puppies import Base, Shelter, Puppy

import decimal as import_decimal
from decimal import Decimal
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
   print "=============================================="
   print "Start"
   print "=============================================="

   print "=============================================="
   print "1. Query all of the puppies and return the "
   print "results in ascending alphabetical order"
   print "=============================================="
   # os.system("pause")

   puppies_list = session.query(Puppy.name)
   for row in puppies_list.order_by(Puppy.name):
      print (row.name)

   print "=============================================="
   print "2. Query all of the puppies that are less than "
   print "six months old organized by the youngest first"
   print "=============================================="
   # os.system("pause")

   today = date.today()
   six_months = today - import_datetime.timedelta(today.month - 6)

   puppies_list = session.query(Puppy.name, Puppy.dateOfBirth).\
                          filter(Puppy.dateOfBirth < six_months).\
                          order_by(Puppy.dateOfBirth)
   for name, dateOfBirth in puppies_list:
      print (name)

   print "=============================================="
   print "3. Query all puppies by ascending weight"
   print "=============================================="
   # os.system("pause")

   puppies_list = session.query(Puppy.name, Puppy.weight).\
                          order_by(Puppy.weight)
   for name, weight in puppies_list:
       print (name, int(weight))

   print "=============================================="
   print "4. Query all puppies grouped by the shelter in which they are staying"
   print "=============================================="
   # os.system("pause")

   puppies_list = session.query(Puppy.name, Shelter.name).\
                          filter(Puppy.shelter_id == Shelter.id).\
                          group_by(Shelter.name, Puppy.name).\
                          order_by(Shelter.name, Puppy.name)
   for shelter_name, puppy_name in puppies_list:
       print (shelter_name, puppy_name)

   print "=============================================="
   print "End"
   print "=============================================="

except:
   session.rollback()
   raise
