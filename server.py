#!/usr/bin/env python3

from flask import Flask, escape, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from email.header import decode_header
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Challenge(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	prefix = db.Column(db.Text)
	nonce_length = db.Column(db.Integer)

	def __init__(self, prefix, nonce_length, id = None):
		self.id = id
		self.prefix = prefix
		self.nonce_length = nonce_length

class ChallengeSchema(ma.Schema):
	class Meta:
		fields = ("id", "prefix", "nonce_length")

challengeSchema = ChallengeSchema()
challengesSchema = ChallengeSchema(many = True)

@app.route('/challenge', methods = ['GET'])
def get_challenges():
	challenges = Challenge.query.all()
	result = challengesSchema.dump(challenges)

	return jsonify(result)

#class Solution(db.Model):
#	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#	hash = db.Column(db.String(64))
#	nonce = db.Column(db.String(64))
#	session_id = db.Column(db.Integer)
#
#	def __init__(self, hash, nonce, session_id):
#		self.hash = hash
#		self.nonce = nonce
#		self.session_id = session_id
#
#class SolutionSchema(ma.Schema):
#	class Meta:
#		feilds = ('hash', 'nonce')
#
#solution_schema = SolutionSchema(strict=True)

def qdecode(string):
	try:
		decoding = decode_header(string)[0]
		return decoding[0].decode(decoding[1])
	except:
		return ""



CHALLENGES = [{
	"id": "0000000000",
	"prefix": "basilisk:0000000000:",
	"nonce_length": 64,
	"solution": {
		"hash": "0001e7ef89881a7e3a00a121cf0741905ee9d63091ed5a603521f3ab3b809289",
		"nonce": "AkD43Rwbud4zUdrfSKWdUnL9zW36CMyBGL8XQwiQnway6wBc1hPqG00cpUtSsq0k",
	}
}]

@app.route('/')
def index():
	return "Hello World"

@app.route('/challenges/')
def list_challenges():
	print(qdecode(request.headers.get("Basilisk-User-Name", "")))
	return jsonify(CHALLENGES)

@app.route('/challenges/<string:id>', methods=['POST'])
def post_challenge(id):
	print(qdecode(request.headers.get("Basilisk-User-Name", "")))
	data = request.get_json()
	if (data["solution"]["hash"] < CHALLENGES[0]["solution"]["hash"]):
		CHALLENGES[0] = data
	return jsonify(CHALLENGES[0])

if __name__ == "__main__":
	app.run(debug=True)
