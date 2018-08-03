from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants')
@app.route('/restaurants/')
def restaurantList():
	return "This page will show all restaurants"

@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu')
def restaurantMenu(restaurant_id):
	return "This page will show restaurant menus"

@app.route('/restaurants/new')
def newRestaurant():
	return "This page will allow you to add a new restaurant"

@app.route('/restaurants/<int:restaurant_id>/edit')
def editRestaurant():
	pass

@app.route('/restaurants/<int:restaurant_id>/delete')
def deleteRestaurant():
	pass

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem():
	pass

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenuItem():
	pass

@app.route('/restaurants/<int:restaurant_id>/menu/new')
def newMenuItem():
	pass


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
