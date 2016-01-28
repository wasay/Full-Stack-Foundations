from sqlalchemy import *
from migrate import *

from sqlalchemy import Table, Column, Integer, String, MetaData

meta = MetaData()

puppy = Table(
    'puppy', meta,
    Column('description', String),
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
