from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import timedelta
import MySQLdb
app = Flask(__name__)

@app.route("/")
def index():
	return render_template("welcome.html")

@app.route("/submit")
def submit():
	return render_template("submit.html")


@app.route("/registerhero", methods = ['GET', 'POST'])
def add_a_hero():
	if request.method == "POST":
		superhero_name = request.form['name']
		superhero_age = request.form['age']
		superhero_height = request.form['height']
		superhero_weight = request.form['weight']

		try:
			my_db = MySQLdb.connect(host = "127.0.0.1", user = "cyber", passwd = "bca4500815", db = "superhero_db", port = 5000)
			cursor = my_db.cursor()
			cursor.execute('''INSERT INTO Superheroes(name, age, height, weight) VALUES (%s,%s,%s,%s)
				''',(superhero_name,superhero_age,superhero_height,superhero_weight,))
		except:
			return("<h1>Error connecting to database</h1>")

		finally:
			print("Record Inserted")	
			my_db.commit()
			return ("<h1>Superhero submitted to database</h1> <br> <a href = '/submit'> Go back </a>")

	return ("<h1>Some error Occured</h1>")



@app.route("/search", methods = ['GET', 'POST'])
def search_for_hero():
	if request.method == "POST":
		heroname = request.form['searchhero']
		print(heroname)
		#try:
		my_db = MySQLdb.connect(host = "127.0.0.1", user = "cyber", passwd = "bca4500815", db = "superhero_db", port = 5000)
		cursor = my_db.cursor()
		cursor.execute('''SELECT name, age, height, weight from Superheroes WHERE name = %s;''',(heroname,))
		attrib = cursor.fetchone()
		a = jsonify(attrib)
		print(a)
		return render_template("heroes.html", name = attrib[0], age = attrib[1], height = attrib[2], weight = attrib[3])
		#except:
		#	return ("<h1> Hero not found in the database. Please consider <a href = '/submit'> adding the hero </a>")
			

	return ("<h1>Some error occured</h1>")





if __name__ == "__main__":
	app.run("127.0.0.1", 5050, debug=True)



