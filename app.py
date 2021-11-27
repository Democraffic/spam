# flask imports
from flask import Flask, request, jsonify


# global Flask instance
app = Flask(__name__)


# Short term api route lookup

API_ROUTE = {
    'text_spam_check': "dummy"
}

@app.route("/")
def index():
    return "Hi! This is the index page of spam utils."


@app.route("/spam/check_description", methods = ['POST', 'GET'])
def check_spam_on_description():

    id = request.json["id"]
    description = request.json["description"]

    response = {
        "id": id,
        "isSpam": description
    }

    return jsonify(response)
