from flask import Flask, render_template, abort
import sqlite3

app = Flask(__name__)


def connect(query, id, year):
#   use this function in the other functions to connect to the database
    conn = sqlite3.connect("waterpolo.db")
    cur = conn.cursor()
    if id is not None and year is None:
        cur.execute(query, id)
    if id and year is not None:
        cur.execute(query, id, year)
    else:
        cur.execute(query)
    results = cur.fetchall()
    return results


@app.route('/') #  app.route maps the URL to this function
#  ending to URL link that displays this 'home' function
def home():
    # returns the corresponding html template
    # the title variable names the tab in the browser
    return render_template("home.html", title="Women's Waterpolo")


@app.route('/countries')
def countries():
    countries = connect('SELECT * FROM Country', None, None)
    return render_template("countries.html", countries=countries, 
                           title="Women's Waterpolo")


@app.route('/country/<int:id>')
def indiv_country(id):
    conn = sqlite3.connect('waterpolo.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Country WHERE id = ?', (id,))
    country = cur.fetchall()
    #country = connect('SELECT * FROM Country WHERE id = ?', (id,), None)
    if country == []:  #  empty list if no result from SQL query
        abort(404)  #  calls the error404 function
    #national_team = connect('SELECT first_name, last_name, image, national_team, player.id FROM Player \
                #WHERE country_id = ? AND national_team = 1', (id,), None)
    cur.execute('SELECT first_name, last_name, image, national_team, player.id FROM Player \
                WHERE country_id = ? AND national_team = 1', (id,))
    national_team = cur.fetchall()
    #former_team = connect('SELECT first_name, last_name, image, national_team, player.id FROM Player \
                #WHERE country_id = ? AND national_team = 0', (id,), None)
    cur.execute('SELECT first_name, last_name, image, national_team, player.id FROM Player \
                WHERE country_id = ? AND national_team = 0', (id,))
    former_team = cur.fetchall()
    return render_template("country.html", country=country, national_team=national_team, 
                           former_team=former_team, title="Women's Waterpolo")


@app.route('/players')
def players():
    # SQL query for getting the top 10 female players in the world
    ranked_players = connect('SELECT Player.id, Player.first_name, Player.last_name, \
                             Player.image, Player.world_ranking, Country.flag FROM Player \
                             Join Country ON Player.country_id=Country.id \
                             WHERE Player.world_ranking IS NOT NULL \
                             ORDER BY Player.world_ranking asc;', None, None)
    # SQL query for getting the rest of the players in the database
    players = connect('SELECT Player.id, Player.first_name, Player.last_name, \
                      Player.image, Country.flag FROM Player \
                      Join Country ON Player.country_id=Country.id \
                      WHERE Player.world_ranking IS NULL;', None, None)
    return render_template("players.html", ranked_players=ranked_players, 
                           players=players, title="Women's Waterpolo")


@app.route('/player/<int:id>')
def indiv_player(id):
    conn = sqlite3.connect('waterpolo.db')
    cur = conn.cursor()
    cur.execute('SELECT Player.first_name, Player.last_name, Player.image, \
                Player.weight, Player.height, Player.world_ranking, Player.cap_number, \
                Country.country, Country.flag, Player.right_hand_dominant, \
                Player.left_hand_dominant, Player.national_team, Country.id FROM Player \
                JOIN Country ON Player.country_id=Country.id \
                WHERE Player.id = ?', (id,))
    player = cur.fetchall()
    if player == [] or id > 9223372036854775807:
        abort(404)
    return render_template("player.html", player=player, title="Women's Waterpolo")


@app.route('/tournaments')
def tournaments():
    conn = sqlite3.connect('waterpolo.db')
    cur = conn.cursor()
    cur.execute('SELECT DISTINCT name_id FROM Tournament')
    tid = cur.fetchall()
    tournaments = []
    for name in tid:
        cur.execute('SELECT Tournament.year, TournamentName.tournament_name, \
                    TournamentName.description, TournamentName.logo, Tournament.id FROM Tournament \
                    JOIN TournamentName ON Tournament.name_id=TournamentName.id \
                    WHERE Tournament.name_id=?', (name))
        tournament = cur.fetchall()
        tournaments.append(tournament)
    return render_template("tournaments.html", tournaments=tournaments, 
                           title="Women's Waterpolo")


@app.route('/tournament/<int:name_id>/<int:year>')
def indiv_tournament(name_id, year):
    conn = sqlite3.connect('waterpolo.db')
    cur = conn.cursor()
    cur.execute('SELECT TournamentName.tournament_name, \
                TournamentName.description, TournamentName.logo, \
                Tournament.name_id, Tournament.year, Tournament.matches \
                FROM Tournament \
                JOIN TournamentName ON Tournament.name_id=TournamentName.id \
                WHERE Tournament.name_id = ? AND Tournament.year = ?',
                (name_id, year,))
    event = cur.fetchall()
    if event == []:
        abort(404)
    cur.execute('SELECT Country.id, Country.country, Country.flag, \
                Tournament.name_id, Tournament.year FROM CountryTournament \
                JOIN Country ON CountryTournament.country_id=Country.id \
                JOIN Tournament ON CountryTournament.tournament_id=Tournament.id \
                WHERE Tournament.name_id = ? AND Tournament.year = ?',
                (name_id, year,))
    teams = cur.fetchall()
    return render_template("tournament.html", event=event, teams=teams,
                           title="Women's Waterpolo")
#  there is a data integrety issue


@app.route('/positions')
def positions():
    # selects all the information from the Position table
    positions = connect('SELECT id, position, image, pos_copyright \
                        FROM Position;', None, None)
    return render_template("positions.html", positions=positions,
                           title="Women's Waterpolo")


@app.route('/position/<int:id>')
def indiv_position(id):
    conn = sqlite3.connect('waterpolo.db')
    cur = conn.cursor()
    cur.execute('SELECT Position.position, Position.image, Position.description FROM Position \
                WHERE Position.id = ?', (id,))
    position = cur.fetchall()
    if position == []:
        abort(404)
    cur.execute('SELECT Player.first_name, Player.last_name, Player.image, Country.flag, Player.id FROM PlayerPosition \
                Join Player ON PlayerPosition.player_id=Player.id \
                Join Country ON Player.country_id=Country.id \
                Join Position ON PlayerPosition.position_id=Position.id WHERE Position.id = ?', (id,))
    position_players = cur.fetchall()
    return render_template("position.html", position=position, position_players=position_players, 
                           title="Women's Waterpolo")


@app.errorhandler(404)
#  app.errorhandler handles invalid route errors
#  the 404 specifies that the error is a page not found error
def page_not_found(error):
    return render_template("error404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)