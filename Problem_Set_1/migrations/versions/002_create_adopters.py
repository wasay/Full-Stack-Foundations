from sqlalchemy import *
from migrate import *

meta = MetaData()


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta.bind = migrate_engine
    adoptors = Table('adoptors', meta,
       Column('id', INTEGER, primary_key=True, nullable=False),
       Column('name', VARCHAR(length=250), nullable=False)
    )
    adoptors.create()
    pass


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine

    adoptors = Table('adoptors', meta, autoload=True)
    adoptors.drop()
    pass
