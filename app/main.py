from flask import Flask, jsonify, make_response
import requests
from bs4 import BeautifulSoup
import logging


app = Flask(__name__)

app.logger.setLevel(logging.INFO)

@app.route('/test', methods=['GET'])
def test():
    response = make_response("hi")
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)