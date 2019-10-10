#!/usr/bin/env python3

from flask import Flask, escape, request, jsonify
from email.header import decode_header

app = Flask(__name__)

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
