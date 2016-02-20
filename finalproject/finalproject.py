from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Fake Restaurants
#restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

#restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]

#Fake Menu Items
#items = [{'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'}]
#item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}


@app.route('/restaurants/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant).order_by('name')
    return jsonify(Restaurants=[i.serialize for i in restaurants])

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantMenuItemJSON(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id, id=menu_id).one()

    return jsonify(MenuItem=menuItem.serialize)

@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        #newItem = Restaurant(name=request.form['name'])
        #session.add(newItem)
        #session.commit()
        flash("new restaurant created!")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newrestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):

    #restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    restaurant = restaurants[restaurant_id-1]

    if request.method == 'POST':
        if request.form['name']:
            restaurant.name = request.form['name']
        #session.add(restaurant)
        #session.commit()
        flash("restaurant has been edited!")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template(
            'editrestaurant.html', restaurant_id=restaurant_id, item=restaurant)
    return output

@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):

    #restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    restaurant = restaurants[restaurant_id-1]

    if request.method == 'POST':
        #session.delete(restaurant)
        #session.commit()
        flash("restaurant has been deleted")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template(
            'deleterestaurant.html', item=restaurant)

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    #restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    #menu_items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)

    restaurant = restaurants[restaurant_id-1]
    menu_items = items

    return render_template('menu.html', restaurant=restaurant, items=menu_items)

@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    #restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

    restaurant = restaurants[restaurant_id-1]

    if request.method == 'POST':
        #newItem = MenuItem(name=request.form['name'],
        #    description=request.form['description'], price=request.form['price'],
        #    course=request.form['course'], restaurant_id=restaurant_id)
        #session.add(newItem)
        #session.commit()
        flash("new menu item created!")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):

    #menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    menuItem = items[menu_id-1]

    if request.method == 'POST':
        if request.form['name']:
            menuItem.name = request.form['name']
            menuItem.description=request.form['description']
            menuItem.price=request.form['price']
            menuItem.course=request.form['course']
        #session.add(menuItem)
        #session.commit()
        flash("menu item has been edited!")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'editmenuitem.html', restaurant=restaurant, menu_id=menu_id, item=menuItem)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    #menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    menuItem = items[menu_id-1]
    if request.method == 'POST':
        #session.delete(menuItem)
        #session.commit()
        flash("menu item has been deleted")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'deletemenuitem.html', restaurant=restaurant, menu_id=menu_id, item=menuItem)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
