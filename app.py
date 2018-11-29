# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify, request
from api.get_forexrate import get_forexrate
from api.get_oilrate import get_oilrate
from api.get_goldvn import get_goldvn
from api.get_news_amway import get_news_amway, get_nutrilite_amway, get_artistry_amway, get_amagram_amway
import logging
app = Flask(__name__)

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == 'foo':
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world! - Check completed", 200

@app.route('/api/amwaynews/news', methods = ['GET'])
def amwaynews():
    json_result = get_news_amway()
    return jsonify(json_result)

@app.route('/api/amwaynews/nutrilite', methods = ['GET'])
def nutrilitenews():
    json_result = get_nutrilite_amway()
    return jsonify(json_result)

@app.route('/api/amwaynews/artistry', methods = ['GET'])
def artistrynews():
    json_result = get_artistry_amway()
    return jsonify(json_result)

@app.route('/api/amwaynews/amagram', methods = ['GET'])
def amagram():
    json_result = get_amagram_amway()
    return jsonify(json_result)

@app.route('/api/forexrate', methods = ['GET'])
def forexrate():
    json_result = get_forexrate('https://www.vietcombank.com.vn/ExchangeRates/ExrateXML.aspx')
    return jsonify(json_result)

@app.route('/api/oilrate', methods = ['GET'])
def oilrate():
    json_result = get_oilrate('http://www.petrolimex.com.vn/')
    return jsonify(json_result)



@app.route('/api/goldvn', methods = ['GET'])
def goldvn():
    json_result = get_goldvn()
    return jsonify(json_result)

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500


if __name__ == '__main__':
    app.run(debug = True)
