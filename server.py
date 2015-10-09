import sqlite3
import time
from search import *
from flask import Flask, request, g, render_template, redirect
app = Flask(__name__)
DATABASE = 'hakks.db'

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
	return db

@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

@app.route("/")
def hello():
	return render_template('home.html')

@app.route("/api/", methods=["POST"])
def receive_hakk():
	form = request.form
	entry = form["search_entry"]
	begins_with = form["begins_with"]
	ends_with = form["ends_with"]

	try:
		this_many_words = int(form["how_many_words"])
	except:
		#Display that not a valid number
		placeholder = None
		this_many_words = None

	if this_many_words:
		results_list = parse_search_entry(entry, 'Synonym', begins_with, ends_with, this_many_words)
	else:
		results_list = parse_search_entry(entry, 'Synonym', begins_with, ends_with)
	if results_list is None:
		results = None
	else:
		results = ', '.join(results_list)

	show = [entry, results]
	return render_template('home.html', results = show)

if __name__ == "__main__":
	app.run()