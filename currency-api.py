# -*- coding: utf-8 -*
from bs4 import BeautifulSoup
import requests
from flask import Flask, redirect, url_for, jsonify, request, render_template, send_from_directory, jsonify, make_response
from flask.helpers import make_response
import sys
reload(sys)
sys.setdefaultencoding('utf8')

base_url = 'https://www.boursorama.com/bourse/devises/taux-de-change-hello-yes-'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36', 'Pragma': 'no-cache'}


def parser(u):
    try:
        r = requests.get(u, headers=headers)
        if r.status_code == 200:
            html = r.text.decode('utf-8')
            soup = BeautifulSoup(html, 'lxml')
            rate = soup.select(  # 10.9554
                '.c-faceplate__price span')[0].text.encode('utf-8')
            currency = soup.select(  # 'MAD'
                '.c-faceplate__price span')[2].text.encode('utf-8').strip(' ')
            variation = soup.select(    # '+0.01%'
                '.c-faceplate__fluctuation span')[0].text.encode('utf-8')
        return rate, currency, variation
    except requests.exceptions.ConnectionError:
        print('Exception while parsing')
        sleep(60)
        return ("400")


apiVersion = 'v0.1'

app = Flask(__name__, static_url_path='')


@app.route("/isalive")
def get_initial_response():
    """Welcome message for the API."""
    message = {
        'apiVersion': apiVersion,
        'status': '200',
        'message': 'Welcome back'
    }
    return jsonify(message)


@app.route('/v1/<string:devise>', methods=['GET'])
def updateLikes(devise):
    URL = base_url + devise + '/'
    try:
        rate, currency, variation = parser(URL)
        print "+" + currency + "<-"
        return make_response(jsonify({"currency": currency, "rate": rate, "variation": variation, "status": "200"}))
    except:
        return make_response(jsonify({"Somthing went wrong": "retry", "Help": "EUR-MAD, EUR-USD, USD-MAD, JPY_EUR, CNY_EUR ...", "status": "400"}))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
