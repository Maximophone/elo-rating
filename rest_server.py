from flask import Flask, jsonify, request, abort, make_response
from elo import Ratings

app = Flask(__name__)

MATCHES_FILE = "./matches.csv"
PLAYERS_FILE = "players.csv"
ratings = Ratings(MATCHES_FILE,PLAYERS_FILE)

basic_menu = [
("Show Ratings","GET","ratings"),
("Show Matches","GET","matches"),
("Add Match","POST","add_match",
	(("Winner Name","pwin"),("Loser name","plose"))),
("Add Player","POST","add_player",
	(("Player Name","pname"),))
]

class Response(object):
	def __init__(self,menu,content=None):
		self._data = {
			"menu":menu,
			"content":content
		}
	@property
	def json(self):
	    return jsonify(self._data)


@app.errorhandler(400)
def bad_request(error):
	return make_response(jsonify({"error": "Bad Request"}),400)

@app.route("/elo/api/v1.0/",methods=["GET"])
def get_index():
	response = Response(basic_menu)
	return response.json

@app.route("/elo/api/v1.0/ratings",methods=["GET"])
def get_ratings():
	response = Response(basic_menu,content=ratings.ratings_string)
	return response.json

@app.route("/elo/api/v1.0/matches",methods=["GET"])
def get_matches():
	response = Response(basic_menu,content=ratings.matches_string)
	return response.json

@app.route("/elo/api/v1.0/add_match",methods=["POST"])
def add_match():
	if not request.json or not "pwin" in request.json or not "plose" in request.json:
		abort(400)
	result = ratings.add_match(request.json["pwin"].lower(),request.json["plose"].lower())
	response = Response(basic_menu,content="Done." if result else "Not Done.")
	return response.json

@app.route("/elo/api/v1.0/add_player",methods=["POST"])
def add_player():
	if not request.json or not "pname" in request.json:
		abort(400)
	result = ratings.add_player(request.json["pname"].lower())
	response = Response(basic_menu,content="Done." if result else "Not Done.")
	return response.json

if __name__ == '__main__':
	app.run(debug=True, port=5656)