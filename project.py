from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Fake Restaurants
#restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

#restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake Menu Items
#items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
#item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}


@app.route('/')
@app.route('/restaurants')
@app.route('/restaurants/')
def restaurantList():
	restaurants = session.query(Restaurant).all()
	return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu')
def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
	return render_template('menu.html', restaurant=restaurant, items=items)


@app.route('/restaurants/new',  methods=['GET', 'POST'])
def newRestaurant():
	if request.method == 'POST':
		newRestaurant = Restaurant(name=request.form['new_restaurant_name'])
		session.add(newRestaurant)
		session.commit()
		return redirect(url_for("restaurantList"))
	else:
		return render_template('newRestaurant.html')


@app.route('/restaurants/<int:restaurant_id>/edit',  methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		restaurant.name = request.form['new_name']
		session.add(restaurant)
		session.commit()
		return redirect(url_for('menu.html', restaurant_id=restaurant_id))
	else:
		return render_template('editRestaurant.html', restaurant=restaurant)

@app.route('/restaurants/<int:restaurant_id>/delete',  methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	unwantedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == "POST":
		session.delete(unwantedRestaurant)
		session.commit()
		return redirect(url_for("restaurantList"))
	return render_template('deleteRestaurant.html', restaurant=unwantedRestaurant)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		if request.form['description']:
			editedItem.description = request.form['description']
		if request.form['price']:
			editedItem.price = request.form['price']
		if request.form['course']:
			editedItem.course = request.form['course']
		session.add(editedItem)
		session.commit()
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	else:
		return render_template('editMenuItem.html',
		restaurant_id=restaurant_id, menu_id=menu_id, editedItem=editedItem)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	 unwantedItem = session.query(MenuItem).filter_by(id=menu_id).one()
	 if request.method == 'POST':
		 session.delete(unwantedItem)
		 session.commit()
		 return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	 else:
		 return render_template("deleteMenuItem.html",restaurant_id=restaurant_id,
		unwantedItem=unwantedItem,
		 menu_id=menu_id)

@app.route('/restaurants/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		newItem = MenuItem(name=request.form['name'],
        description=request.form['description'],
		price = request.form['price'],
		course = request.form['course'],
		restaurant_id=restaurant_id)
		session.add(newItem)
		session.commit()
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	else:
		return render_template('newMenuItem.html', restaurant_id=restaurant_id, restaurant=restaurant)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
