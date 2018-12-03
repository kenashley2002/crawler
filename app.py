# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify, request
import requests
from api.get_weather import get_weather
from api.get_forexrate import get_forexrate
from api.get_oilrate import get_oilrate
from api.get_goldvn import get_goldvn
from api.get_news_amway import get_news_amway, get_nutrilite_amway, get_artistry_amway, get_amagram_amway
from api.get_quotes import get_quotes
from webview.get_test_add_cart import get_test_add_cart
import logging

# Init Flask
app = Flask(__name__)

# Secret Key
chatfuel_bot_id = '5bf6673076ccbc3d548ff901'
chatfuel_key = 'zPgOSM7QJ2LVineaMDX4t43FTiVn0krC7uqjhZkzbWIu249sP1T4zssLtl5vtsnq'

# Verify app on web
@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == 'crawler':
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world! - Check completed", 200

# API Weather
@app.route('/api/weather', methods = ['GET'])
def weather():
    city = request.args.get('city')
    json_result = get_weather(city)
    return jsonify(json_result)

# API for Amway Inc.
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

# API Great Quotes
@app.route('/api/quotes', methods = ['GET'])
def quotes():
    json_result = get_quotes()
    return jsonify(json_result)

# API Forex Rates
@app.route('/api/forexrate', methods = ['GET'])
def forexrate():
    json_result = get_forexrate()
    return jsonify(json_result)

# API Oil Rates
@app.route('/api/oilrate', methods = ['GET'])
def oilrate():
    json_result = get_oilrate()
    return jsonify(json_result)

# API VN Gold Rates
@app.route('/api/goldvn', methods = ['GET'])
def goldvn():
    json_result = get_goldvn()
    return jsonify(json_result)

# -*- Begin Webview Templates -*-
@app.route('/webview/show-buttons', methods = ['GET'])
def show_buttons():
    json_result = get_test_add_cart()
    return jsonify(json_result)

@app.route('/webview/show-webview', methods = ['GET'])
def show_webview():
    return render_template('webview.html')

@app.route('/webview/broadcast-to-chatfuel', methods = ['POST'])
def broadcast_to_chatfuel():
    botId = chatfuel_bot_id
    userId = '1940186179401012'
    token = chatfuel_key
    blockId = '5bf9155976ccbc0196b80eeb'
    fields = [k for k in request.form]
    values = [request.form[k] for k in request.form]
    data = dict(zip(fields, values))
    query = requests.get("https://api.chatfuel.com/bots/{botId}/users/{userId}/send?chatfuel_token={token}&chatfuel_block_id={blockId}".format(botId = botId, userId = userId, token = token, blockId = blockId),
                         params = data)
    return jsonify(data), query.url
# -*- End Webview -*-

# Logging for error
@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

if __name__ == '__main__':
    app.run(debug = True)
