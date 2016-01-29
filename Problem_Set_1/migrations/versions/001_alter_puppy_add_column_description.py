from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    puppy = Table('puppy', metadata, Column("description", String), extend_existing=True)
    puppy.c.description.alter(type=String)
    pass


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pass
