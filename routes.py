from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html", title="Waterpolo Players") #title variable names the tab in the website


@app.route('/countries')
def countries():
    conn = sqlite3.connect('waterpolo.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Country')
    countries = cur.fetchall()
    return render_template("countries.html", countries=countries, title="Waterpolo Players")


@app.route('/country/<int:id>')
def indiv_country(id):
    conn = sqlite3.connect('waterpolo.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Country WHERE id = ?', (id,))
    country = cur.fetchone()
    #cur.execute('SELECT ') #finish query (part of iteration 2)
    return render_template("country.html", country=country, title="Waterpolo Players")


@app.route('/players')
def players():
    conn = sqlite3.connect('waterpolo.db')
    cur = conn.cursor()
    cur.execute('SELECT Player.id, Player.first_name, Player.last_name, Player.image, Player.world_ranking, Country.flag FROM Player Join Country ON Player.country_id=Country.id WHERE Player.world_ranking IS NOT NULL;')
    ranked_players = cur.fetchall()
    cur.execute('SELECT Player.id, Player.first_name, Player.last_name, Player.image, Country.flag FROM Player Join Country ON Player.country_id=Country.id WHERE Player.world_ranking IS NULL;')
    players = cur.fetchall()
    #have the 'none' disappear
    #world ranking still required in further iterations (could have interaction from the user how they want the data ordered)
    return render_template("players.html", ranked_players=ranked_players, players=players, title="Waterpolo Players")


@app.route('/player/<int:id>')
def indiv_player(id):
    return render_template("______", title="Waterpolo Players") #return something


@app.route('/tournaments')
def tournaments():
    conn = sqlite3.connect('waterpolo.db')
    cur = conn.cursor()
    cur.execute('SELECT DISTINCT tournament_name, description, logo FROM Tournament;')
    tournaments = cur.fetchall()
    return render_template("tournaments.html", tournaments=tournaments, title="Waterpolo Players")


@app.route('/tournament/<int:id>')
def indiv_tournament(id):
    return render_template("______", title="Waterpolo Players") #return something


@app.route('/positions')
def positions():
    return render_template("______", title="Waterpolo Players") #return something


@app.route('/position/<int:id>')
def indiv_position(id):
    return render_template("______", title="Waterpolo Players") #return something


if __name__ == "__main__":
    app.run(debug=True)