from sqlalchemy import *
from migrate import *
from migrate.changeset.constraint import ForeignKeyConstraint

meta = MetaData()

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta.bind = migrate_engine

    shelter_puppies = Table('shelter_puppies', meta,
        Column('id', INTEGER, primary_key=True, nullable=False),
        Column('shelter_id', INTEGER),
        Column('puppy_id', INTEGER)
    )
    shelter_puppies.create()

    shelter = Table('shelter', meta, autoload=True)
    puppy = Table('puppy', meta, autoload=True)
    shelter_puppies = Table('shelter_puppies', meta, autoload=True)

    cons1 = ForeignKeyConstraint([shelter_puppies.c.shelter_id], [shelter.c.id])
    cons1.create()

    cons2 = ForeignKeyConstraint([shelter_puppies.c.puppy_id], [puppy.c.id])
    cons2.create()
    pass


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine

    shelter = Table('shelter', meta, autoload=True)
    puppy = Table('puppy', meta, autoload=True)
    shelter_puppies = Table('shelter_puppies', meta, autoload=True)

    cons1 = ForeignKeyConstraint([shelter_puppies.c.shelter_id], [shelter.c.id])
    cons1.drop()

    cons2 = ForeignKeyConstraint([shelter_puppies.c.puppy_id], [puppy.c.id])
    cons2.drop()

    shelter_puppies.drop()
    pass
