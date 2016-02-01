from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from puppies import Shelter, Base, Puppy
# from flask.ext.sqlalchemy import SQLAlchemy

from random import randint
import datetime
import random


engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

male_names = ["Noah A", "Liam B", "Mason C", "Jacob C"]

female_names = ['Emma A', 'Olivia B', 'Sophia C', 'Isabella D']

adoptors = Table('adoptors', meta, autoload=True)
puppy_adoptors = Table('puppy_adoptors', meta, autoload=True)
try:

   for i, x in enumerate(male_names):
	  adoptor = Adoptors(id=None, name=x)
	  session.add(adoptor)
	  session.commit()

   for i, x in enumerate(female_names):
	  adoptor = Adoptors(id=None, name=x)
	  session.add(adoptor)
	  session.commit()


   puppies_list = session.query(Puppy.id, Puppy.name).order_by(Puppy.name)
   for i, row in enumerate(puppies_list):
	  print i
	  print row
	  if i < count(male_names):
		 indx = i
		 puppy_adopt = PuppyAdoptor(id=None, row.id, male_names[indx])
		 session.add(puppy_adopt)
		 session.commit()
	  if i > count(male_names) + i < count(female_names):
		 indx = i - count(male_names)
		 puppy_adopt = PuppyAdoptor(id=None, row.id, female_names[indx])
		 session.add(puppy_adopt)
		 session.commit()
except:
   session.rollback()
   raise
