from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from database_setup import Restaurant, Base, MenuItem

import lotsofmenus

print "CRUD - Lesson 1 - Import"

engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

print "CRUD - Lesson 1 - Session"

# Menu for Pizza Palace
myFirstRestaurant = Restaurant(name="Pizza Palace")

session.add(myFirstRestaurant)
session.commit()

print "CRUD - Lesson 1 - First Restaurant"

cheesepizza = MenuItem(name="Cheese Pizza", description="Made with all natural"
                       "ingredients and fresh mozzarella",
                       price="$8.99", course="Entree",
                       restaurant=myFirstRestaurant)

session.add(cheesepizza)
session.commit()

print "CRUD - Lesson 1 - Cheese Pizza"

firstResult = session.query(Restaurant).first()
print firstResult.name

print "CRUD - Lesson 1 - First Result"

items = session.query(MenuItem).all()
for item in items:
    print item.name

veggieBurgers = session.query(MenuItem).filter_by(name='Veggie Burger')
for veggieBurger in veggieBurgers:
    print veggieBurger.id
    print veggieBurger.price
    print veggieBurger.restaurant.name
    print "\n"

UrbanVeggieBurger = session.query(MenuItem).filter_by(id='8').one()
UrbanVeggieBurger.price = '$2.99'
session.add(UrbanVeggieBurger)
session.commit()

spinach = session.query(MenuItem).filter_by(name='Spinach Ice Cream').one()
session.delete(spinach)
session.commit()

print "CRUD - Lesson 1 - End"
