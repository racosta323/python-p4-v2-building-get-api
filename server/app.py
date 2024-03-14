# server/app.py

#routes go here

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

    #can make more code succinct by replacing all with list comprehension below
    # db_games = Game.query.all()
    # games = []
    # for game in db_games:

        #replaced by SerializerMixin
        # game_dict = {
        #     "title": game.title,
        #     "genre": game.genre,
        #     "platform": game.platform,
        #     "price": game.price,
        # }

       
        # game_dict = game.to_dict()
        # games.append(game_dict)
        
    games = [game.to_dict() for game in Game.query.all()]

        #jsonify is a method in Flask that serializes args as json and
        #returns a Response object; accepts lists or dictionaries
    
    #no longer need to use jsonify if using mixin!
    # response = make_response(jsonify(games), 200)
    response = make_response(games, 200)


    # add this after 200 {"Content-Type": "application/json"} UNLESS jsonify is used (which includes)
    #default content-type is text/html -- sent as a response header; server only sends json so updates

    return response

@app.route('/games/<int:id>')
def game_by_id(id):
    #gets one game from db
    game = Game.query.filter(Game.id == id).first()

    game_dict = game.to_dict()
    #using SerializerMixin replaces having to convert to dict
    # game_dict = {
    #     "title": game.title,
    #     "genre": game.genre,
    #     "platform": game.platform,
    #     "price": game.price
    # }

    response = make_response(game_dict, 200)
    return response

@app.route('/games/users/<int:id>')
def game_users_by_id(id):
    game = Game.query.filter(Game.id == id).first()
    #can be simplified using a list comprehension (below)
    # users = []
    # #game.reviews found in Game class
    # for review in game.reviews:
    #     user = review.user
    #     #exclude reviews in to_dict rules
    #     user_dict=user.to_dict(rules=('-reviews',))
    #     users.append(user_dict)   

    #setting up an assoc proxy in Games class to add user from each review replaces this:
    # users = [review.user.to_dict(rules=('-reviews',)) for review in game.reviews]
    users = [user.to_dict() for user in game.users]

    response = make_response(users, 200)
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)

