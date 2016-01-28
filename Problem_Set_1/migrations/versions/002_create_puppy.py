from sqlalchemy import *
from migrate import *

from sqlalchemy import create_engine
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base
# from migrate.changeset.constraint import ForeignKeyConstraint
from sqlalchemy import Table, Column, Integer, String, MetaData

engine = create_engine('sqlite:///puppyshelter.db')

meta = MetaData(engine)

shelter = Table(
	'shelter', meta,
	autoload=True,
)

puppy = Table(
    'puppy', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(250), nullable=False),
    Column('gender', String(6), nullable=False),
    Column('dateOfBirth', Date),
    Column('picture', String),
    Column('weight', Numeric(3)),
    Column('description', String),
    Column('shelter_id', Integer, ForeignKey('shelter.id')),
    shelter = relationship(shelter),
)

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta.bind = migrate_engine
    puppy.create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    puppy.drop()
