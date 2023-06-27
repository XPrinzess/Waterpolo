from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html", title="Waterpolo Players") #title variable names the tab in the website


@app.route('/countries')
def countries():
    #need a sql query
    return render_template("countries.html")


@app.route('/country/<int:id>')
def indiv_country(id):
    return render_template("______") #return something


@app.route('/players')
def players():
    return render_template("______") #return something


@app.route('/player/<int:id>')
def indiv_player(id):
    return render_template("______") #return something


@app.route('/tournaments')
def tournaments():
    return render_template("______") #return something


@app.route('/tournament/<int:id>')
def indiv_tournament(id):
    return render_template("______") #return something


@app.route('/positions')
def positions():
    return render_template("______") #return something


@app.route('/position/<int:id>')
def indiv_position(id):
    return render_template("______") #return something




""" @app.route('/all_pizzas')
def all_pizzas():
    conn = sqlite3.connect('pizza.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Pizza')
    pizzas = cur.fetchall()
    return render_template('all_pizzas.html', pizzas=pizzas)


@app.route('/pizza/<int:id>')
def pizza(id):
    conn = sqlite3.connect('pizza.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Pizza WHERE id = ?', (id,))
    pizza = cur.fetchone()
    cur.execute('SELECT name FROM Base WHERE id = ?', (pizza[4],))
    base = cur.fetchone()
    cur.execute('SELECT name FROM Topping WHERE id IN(SELECT tid FROM PizzaTopping WHERE pid = ?)', (id,))
    topping = cur.fetchall()
    return render_template('pizza.html', pizza=pizza, base=base, topping=topping)
"""
if __name__ == "__main__":
    app.run(debug=True)