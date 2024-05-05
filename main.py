from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect()
csrf.init_app(app) # Compliant

@app.route('/test', methods=['GET'])
def test():
    return "hi"
if __name__ == '__main__':
    app.run(debug=True)