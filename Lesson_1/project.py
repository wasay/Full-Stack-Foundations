from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    output = ''
    if restaurant != False:
        for i in items:
            output += i.name
            output += '</br>'
            output += i.price
            output += '</br>'
            output += i.description
            output += '</br>'
            output += ('<a href="/restaurants/%s/menuitems/edit/%s/">Edit</a>') % (restaurant_id, i.id)
            output += '&nbsp;&nbsp;'
            output += ('<a href="/restaurants/%s/menuitems/delete/%s/">Delete</a>') % (restaurant_id, i.id)
            output += '</br>'
            output += '</br>'

        output += ('<a href="/restaurants/%s/menuitems/new/">Add a menu item</a>') % (restaurant_id)
    else:
        output += "Unable to locate restaurant"
    output += "<p>&nbsp;</p>"

    return output

# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/menuitems/new/')

def newMenuItem(restaurant_id):
    # return "page to create a new menu item. Task 1 complete!"
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    output = ''
    if restaurant != False:
        output += "<h1>Add a Menu Item</h1>"
        output += ('''<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/menuitems/add/'>''') % (restaurant_id)
        output += '''Name: <input name="menu_item_name" type="text" value="" placeholder="New Menu Item" >'''
        output += '''<br><br>'''
        output += '''<input type="submit" value="Create Menu Item">'''
        output += '''</form>'''
    else:
        output += "Unable to locate restaurant"
    output += "<p>&nbsp;</p>"
    return output

# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/menuitems/edit/<int:menu_id>/')

def editMenuItem(restaurant_id, menu_id):
    # return "page to edit a menu item. Task 2 complete!"
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id,id=menu_id).one()

    output = ''
    if items != False:
        output += "<h1>Edit Menu Item</h1>"
        output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/<int:restaurant_id>/menuitems/update/<int:menu_id>/'>'''
        output += ('''Name: <input name="menu_item_name" type="text" value="%s" placeholder="Update Menu Item" >''') % (items.name)
        output += '''<br><br>'''
        output += '''<input type="submit" value="Update">'''
        output += '''</form>'''
    else:
        output += "Unable to locate the menu item"
    output += "<p>&nbsp;</p>"
    return output

# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/menuitems/delete/<int:menu_id>/')

def deleteMenuItem(restaurant_id, menu_id):
    # return "page to delete a menu item. Task 3 complete!"

    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id,id=menu_id).one()

    output = ''
    if items != False:
        output += "<h1>Delete Menu Item</h1>"
        output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/<int:restaurant_id>/menuitems/remove/<int:menu_id>/'>'''
        output += ('''Name: %s''') % (items.name)
        output += '''<br><br>'''
        output += '''<input type="submit" value="Delete">'''
        output += '''</form>'''
    else:
        output += "Unable to locate the menu item"
    output += "<p>&nbsp;</p>"

    return output

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
