## File autogenerated by genmodel.py

from sqlalchemy import *

meta = MetaData()

puppy = Table('puppy', meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=250), nullable=False),
    Column('gender', VARCHAR(length=6), nullable=False),
    Column('dateOfBirth', DATE),
    Column('picture', VARCHAR),
    Column('weight', NUMERIC(precision=3)),
    Column('shelter_id', INTEGER),
)

shelter = Table('shelter', meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=80), nullable=False),
    Column('address', VARCHAR(length=250)),
    Column('city', VARCHAR(length=80)),
    Column('state', VARCHAR(length=20)),
    Column('zipCode', VARCHAR(length=10)),
    Column('website', VARCHAR),
)
