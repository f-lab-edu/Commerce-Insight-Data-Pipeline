from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/test', methods=['GET'])
def test():
    return "hi"
if __name__ == '__main__':
    app.run(debug=True)