from sqlalchemy import *
from migrate import *

from sqlalchemy import Table, Column, Integer, String, MetaData

meta = MetaData()

shelter = Table(
    'shelter', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(80), nullable=False),
    Column('address', String(250)),
    Column('city', String(80)),
    Column('state', String(20)),
    Column('zipCode', String(10)),
    Column('website', String),
)

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta.bind = migrate_engine
    shelter.create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    shelter.drop()
