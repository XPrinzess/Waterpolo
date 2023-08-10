from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


# use this function in the other functions to connect to the database
# def connect():
#    conn = sqlite3.connect('waterpolo.db')
#    cur = conn.cursor()


@app.route('/')
def home():
    return render_template("home.html", title="Waterpolo Players")  # title variable names the tab in the website


@app.route('/countries')
def countries():
    conn = sqlite3.connect('waterpolo.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Country;')
    countries = cur.fetchall()
    return render_template("countries.html", countries=countries, title="Waterpolo Players")


@app.route('/country/<int:id>')
def indiv_country(id):
    conn = sqlite3.connect('waterpolo.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Country WHERE id = ?', (id,))
    country = cur.fetchall()
    cur.execute('SELECT first_name, last_name, image, national_team, player.id FROM Player WHERE country_id = ? AND national_team = 1', (id,))
    national_team = cur.fetchall()
    cur.execute('SELECT first_name, last_name, image, national_team, player.id FROM Player WHERE country_id = ? AND national_team = 0', (id,))
    former_team = cur.fetchall()
    #get template to only print 'former team' or 'national team' once
    return render_template("country.html", country=country, national_team=national_team, former_team=former_team, title="Waterpolo Players")


@app.route('/players')
def players():
    conn = sqlite3.connect('waterpolo.db')
    cur = conn.cursor()
    cur.execute('SELECT Player.id, Player.first_name, Player.last_name, Player.image, Player.world_ranking, Country.flag FROM Player Join Country ON Player.country_id=Country.id WHERE Player.world_ranking IS NOT NULL;')
    ranked_players = cur.fetchall()
    cur.execute('SELECT Player.id, Player.first_name, Player.last_name, Player.image, Country.flag FROM Player Join Country ON Player.country_id=Country.id WHERE Player.world_ranking IS NULL;')
    players = cur.fetchall()
    # world ranking still required in further iterations (could have interaction from the user how they want the data ordered)
    return render_template("players.html", ranked_players=ranked_players, players=players, title="Waterpolo Players")


@app.route('/player/<int:id>')
def indiv_player(id):
    conn = sqlite3.connect('waterpolo.db')
    cur = conn.cursor()
    cur.execute('SELECT Player.first_name, Player.last_name, Player.image, Player.weight, Player.height, Player.world_ranking, Player.cap_number, Country.country, Country.flag, Player.right_hand_dominant, Player.left_hand_dominant, Player.national_team, Country.id FROM Player JOIN Country ON Player.country_id=Country.id WHERE Player.id = ?', (id,))
    player = cur.fetchall()
    return render_template("player.html", player=player, title="Waterpolo Players")


@app.route('/tournaments')
def tournaments():
    conn = sqlite3.connect('waterpolo.db')
    cur = conn.cursor()
    cur.execute('SELECT DISTINCT tournament_name, description, logo FROM Tournament;')
    tournaments = cur.fetchall()

    # change sqlite database (after checking that er diagram #8 is correct)
    # write query for tournaments page

    cur.execute('SELECT year FROM Tournament;')
    years = cur.fetchall()
    return render_template("tournaments.html", tournaments=tournaments, years=years, title="Waterpolo Players")


@app.route('/tournament/<int:id>')
def indiv_tournament(id):
    return render_template("______", title="Waterpolo Players") #return something


@app.route('/positions')
def positions():
    conn = sqlite3.connect('waterpolo.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Position;')
    positions = cur.fetchall()
    return render_template("positions.html", positions=positions, title="Waterpolo Players")


@app.route('/position/<int:id>')
def indiv_position(id):
    conn = sqlite3.connect('waterpolo.db')
    cur = conn.cursor()
    cur.execute('SELECT Position.position, Position.image, Position.pos_copyright FROM Position WHERE Position.id = ?', (id,))
    position = cur.fetchall()
    cur.execute('SELECT Player.first_name, Player.last_name, Player.image, Country.flag, Player.id FROM PlayerPosition Join Player ON PlayerPosition.player_id=Player.id Join Country ON Player.country_id=Country.id Join Position ON PlayerPosition.position_id=Position.id WHERE Position.id = ?', (id,))
    position_players = cur.fetchall()
    return render_template("position.html", position=position, position_players=position_players, title="Waterpolo Players")


if __name__ == "__main__":
    app.run(debug=True)