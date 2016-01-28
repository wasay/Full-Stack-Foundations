import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from decimal import *

from puppies import Shelter, Base, Puppy

import datetime as import_datetime
from datetime import date
from datetime import datetime

import puppyadd
# import puppypopulator

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

print "=============================================="
print "View Start"
print "=============================================="

print "=============================================="
print "1. Query all of the puppies and return the "
print "results in ascending alphabetical order"
print "=============================================="
os.system("pause")

for name in session.query(Puppy.name).group_by(Puppy.name).order_by(Puppy.name):
    print (name)

print "=============================================="
print "2. Query all of the puppies that are less than "
print "six months old organized by the youngest first"
print "=============================================="
os.system("pause")

today = date.today()
six_months = today - import_datetime.timedelta(today.month - 6)
puppies_list = session.query(Puppy.name, Puppy.dateOfBirth)
six_months_old_puppies = puppies_list.filter(Puppy.dateOfBirth < six_months)
for name, dateOfBirth in six_months_old_puppies.order_by(Puppy.dateOfBirth):
    #date_of_birth_combine = datetime.combine(dateOfBirth, datetime.min.time())
    #date_of_birth =  import_datetime.timedelta(today.month - date_of_birth_combine.month)
    print (name)

print "=============================================="
print "3. Query all puppies by ascending weight"
print "=============================================="
os.system("pause")

for puppy in session.query(Puppy).order_by(Puppy.weight):
    print (puppy.name, puppy.weight.quantize(Decimal('0.01')),
           puppy.shelter_id)

print "=============================================="
print "4. Query all puppies grouped by the shelter in which they are staying"
print "=============================================="
os.system("pause")
pets_shelter = session.query(Puppy, Shelter)
pets_shelter_group = pets_shelter.group_by(Shelter.id, Puppy.id)
for pet in pets_shelter_group.order_by(Shelter.name, Puppy.name):
    print (pet.Shelter.name, pet.Puppy.name)

print "=============================================="
print "View End"
print "=============================================="
