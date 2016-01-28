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


# Add Shelters
shelter1 = Shelter(name="Oakland Animal Services", address="1101 29th Ave",
                   city="Oakland", state="California", zipCode="94601",
                   website="oaklandanimalservices.org")
session.add(shelter1)

shelter2 = Shelter(name="San Francisco SPCA Mission Adoption Center",
                   address="250 Florida St", city="San Francisco",
                   state="California", zipCode="94103", website="sfspca.org")
session.add(shelter2)

# Commit new shelters
session.commit()

# Add Puppies

male_names = ["Bailey", "Max", "Charlie"]

female_names = ['Bella', 'Lucy', 'Molly']

puppy_images = ["http://pixabay.com/get/da0c8c7e4aa09ba3a353/1433170694/"
                "dog-785193_1280.jpg?direct", "http://pixabay.com/get/"
                "6540c0052781e8d21783/1433170742/dog-280332_1280.jpg?direct",
                "http://pixabay.com/get/8f62ce526ed56cd16e57/1433170768/"
                "pug-690566_1280.jpg?direct"]

# This method will make a random age for each puppy between 0-18 months
# (approx.) old from the day the algorithm was run.


def CreateRandomAge():
    today = datetime.date.today()
    days_old = randint(0, 540)
    birthday = today - datetime.timedelta(days=days_old)
    return birthday

# This method will create a random weight between 1.0-40.0 pounds
# (or whatever unit of measure you prefer)


def CreateRandomWeight():
    return random.uniform(1.0, 40.0)

for i, x in enumerate(male_names):
    new_puppy = Puppy(id=None, name=x, gender="male", dateOfBirth=CreateRandomAge(),
                      picture=random.choice(puppy_images),
                      shelter_id=randint(1, 2), weight=CreateRandomWeight())
    session.add(new_puppy)
    session.commit()

for i, x in enumerate(female_names):
    new_puppy = Puppy(id=None, name=x, gender="female", dateOfBirth=CreateRandomAge(),
                      picture=random.choice(puppy_images),
                      shelter_id=randint(1, 2), weight=CreateRandomWeight())
    session.add(new_puppy)
    session.commit()
