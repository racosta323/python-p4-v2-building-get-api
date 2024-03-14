# server/app.py

from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# configuration that has JSON responses print on separate lines with indentation; set false for human eyes
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

# start building your API here
@app.route('/games')
def games():
    db_games = Game.query.all()
    games = []
    for game in db_games:
        game_dict = {
            "title": game.title,
            "genre": game.genre,
            "platform": game.platform,
            "price": game.price,
        }
        games.append(game_dict)
        #jsonify is a method in Flask that serializes args as json and
        #returns a Response object; accepts lists or dictionaries
    response = make_response(jsonify(games), 200)
    # add this after 200 {"Content-Type": "application/json"} UNLESS jsonify is used (which includes)
    #default content-type is text/html -- sent as a response header; server only sends json so updates

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)

