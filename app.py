# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
import logging
app = Flask(__name__)

# --- Begin crawler ForexRate ----
def get_forexrate(url):
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    item = []
    for child in soup.exratelist.find_all('exrate'):
        item += [{child['currencycode']: [
            child['currencyname'], child['buy'], child['transfer'], child['sell']
        ]}]
    return item
# --- End crawler Forexrate ---


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == 'foo':
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world! - Check completed", 200

@app.route('/api/forexrate', methods = ['GET'])
def forexrate():
    get_result = get_forexrate('https://www.vietcombank.com.vn/ExchangeRates/ExrateXML.aspx')
    json_result = {
        'messages': [
            {
                'attachment': {
                    'type': 'template',
                    'payload': {
                        'template_type': 'generic',
                        'image_aspect_ratio': 'square',
                        'elements': [
                            {
                            'title': get_result[0]['AUD'][0],
                                "image_url": 'http://blog.buyforexonline.com/wp-content/uploads/2016/07/23463208_s-1.jpg',
                                'subtitle': 'Mua: ' + str(get_result[0]['AUD'][1]) + ' Bán: ' + str(get_result[0]['AUD'][3])
                            },
                            {
                                'title': get_result[1]['CAD'][0],
                                "image_url": 'http://blog.buyforexonline.com/wp-content/uploads/2016/07/23463208_s-1.jpg',
                                'subtitle': 'Mua: ' + str(get_result[1]['CAD'][1]) + ' Bán: ' + str(
                                    get_result[1]['CAD'][3])
                            },
                            {
                                'title': get_result[4]['EUR'][0],
                                "image_url": 'http://blog.buyforexonline.com/wp-content/uploads/2016/07/23463208_s-1.jpg',
                                'subtitle': 'Mua: ' + str(get_result[4]['EUR'][1]) + ' Bán: ' + str(
                                    get_result[4]['EUR'][3])
                            },
                            {
                                'title': get_result[6]['HKD'][0],
                                "image_url": 'http://blog.buyforexonline.com/wp-content/uploads/2016/07/23463208_s-1.jpg',
                                'subtitle': 'Mua: ' + str(get_result[6]['HKD'][1]) + ' Bán: ' + str(
                                    get_result[6]['HKD'][3])
                            },
                            {
                                'title': get_result[8]['JPY'][0],
                                "image_url": 'http://blog.buyforexonline.com/wp-content/uploads/2016/07/23463208_s-1.jpg',
                                'subtitle': 'Mua: ' + str(get_result[8]['JPY'][1]) + ' Bán: ' + str(
                                    get_result[8]['JPY'][3])
                            },
                            {
                                'title': get_result[11]['MYR'][0],
                                "image_url": 'http://blog.buyforexonline.com/wp-content/uploads/2016/07/23463208_s-1.jpg',
                                'subtitle': 'Mua: ' + str(get_result[11]['MYR'][1]) + ' Bán: ' + str(
                                    get_result[11]['MYR'][3])
                            },
                            {
                                'title': get_result[16]['SGD'][0],
                                "image_url": 'http://blog.buyforexonline.com/wp-content/uploads/2016/07/23463208_s-1.jpg',
                                'subtitle': 'Mua: ' + str(get_result[16]['SGD'][1]) + ' Bán: ' + str(
                                    get_result[16]['SGD'][3])
                            },
                            {
                                'title': get_result[17]['THB'][0],
                                "image_url": 'http://blog.buyforexonline.com/wp-content/uploads/2016/07/23463208_s-1.jpg',
                                'subtitle': 'Mua: ' + str(get_result[17]['THB'][1]) + ' Bán: ' + str(
                                    get_result[17]['THB'][3])
                            },
                            {
                                'title': get_result[18]['USD'][0],
                                "image_url": 'http://blog.buyforexonline.com/wp-content/uploads/2016/07/23463208_s-1.jpg',
                                'subtitle': 'Mua: ' + str(get_result[18]['USD'][1]) + ' Bán: ' + str(
                                    get_result[18]['USD'][3])
                            }
                        ]
                    }
                }
            }
        ]
    }
    return jsonify(json_result)

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500


if __name__ == '__main__':
    app.run(debug = True)
