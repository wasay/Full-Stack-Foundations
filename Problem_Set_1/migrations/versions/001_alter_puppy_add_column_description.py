from sqlalchemy import *
from migrate import *

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta = MetaData(bind=migrate_engine)
    puppy = Table('puppy', meta, autoload=True)
    col_description = Column('description', String(128))
    col_description.create(puppy)
    col_special_needs = Column('special_needs', String(128))
    col_special_needs.create(puppy)
    pass


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta = MetaData(bind=migrate_engine)
    puppy = Table('puppy', meta, autoload=True)
    puppy.c.description.drop()
    puppy.c.special_needs.drop()
    pass
