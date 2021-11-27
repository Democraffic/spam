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
