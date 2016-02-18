from flask import Flask, render_template, request, redirect, url_for
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

    return render_template('menu.html', restaurant=restaurant, items = items)

# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/menuitems/new/', methods=['GET', 'POST'])

def newMenuItem(restaurant_id):
    # return "page to create a new menu item. Task 1 complete!"
    if request.method == 'POST':
        newItem = MenuItem(
            name=request.form['name'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)

# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/menuitems/<int:menu_id>/edit/', methods=['GET', 'POST'])

def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)

# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/menuitems/<int:menu_id>/delete/')

def deleteMenuItem(restaurant_id, menu_id):
    # return "page to delete a menu item. Task 3 complete!"

    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id,id=menu_id).one()

    output = ''
    if items != False:
        output += "<h1>Delete Menu Item</h1>"
        output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/<int:restaurant_id>/menuitems/<int:menu_id>/remove/'>'''
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
