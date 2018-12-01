import requests
from bs4 import BeautifulSoup

def get_forexrate():
    url = 'https://www.vietcombank.com.vn/ExchangeRates/ExrateXML.aspx'
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    get_result = []
    for child in soup.exratelist.find_all('exrate'):
        get_result += [{child['currencycode']: [
            child['currencyname'], child['buy'], child['transfer'], child['sell']
        ]}]
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
                                'title': get_result[18]['USD'][0],
                                "image_url": 'http://blog.buyforexonline.com/wp-content/uploads/2016/07/23463208_s-1.jpg',
                                'subtitle': 'Mua: ' + str(get_result[18]['USD'][1]) +' |' + ' Bán: ' + str(
                                    get_result[18]['USD'][3])
                            },
                            {
                            'title': get_result[0]['AUD'][0],
                                "image_url": 'http://blog.buyforexonline.com/wp-content/uploads/2016/07/23463208_s-1.jpg',
                                'subtitle': 'Mua: ' + str(get_result[0]['AUD'][1]) + ' |' + ' Bán: ' + str(get_result[0]['AUD'][3])
                            },
                            {
                                'title': get_result[1]['CAD'][0],
                                "image_url": 'http://blog.buyforexonline.com/wp-content/uploads/2016/07/23463208_s-1.jpg',
                                'subtitle': 'Mua: ' + str(get_result[1]['CAD'][1]) + ' |' + ' Bán: ' + str(
                                    get_result[1]['CAD'][3])
                            },
                            {
                                'title': get_result[2]['CHF'][0],
                                "image_url": 'http://blog.buyforexonline.com/wp-content/uploads/2016/07/23463208_s-1.jpg',
                                'subtitle': 'Mua: ' + str(get_result[2]['CHF'][1]) +' |' + ' Bán: ' + str(
                                    get_result[2]['CHF'][3])
                            },
                            {
                                'title': get_result[4]['EUR'][0],
                                "image_url": 'http://blog.buyforexonline.com/wp-content/uploads/2016/07/23463208_s-1.jpg',
                                'subtitle': 'Mua: ' + str(get_result[4]['EUR'][1]) +' |' + ' Bán: ' + str(
                                    get_result[4]['EUR'][3])
                            },
                            {
                                'title': get_result[5]['GBP'][0],
                                "image_url": 'http://blog.buyforexonline.com/wp-content/uploads/2016/07/23463208_s-1.jpg',
                                'subtitle': 'Mua: ' + str(get_result[5]['GBP'][1]) +' |' + ' Bán: ' + str(
                                    get_result[5]['GBP'][3])
                            },
                            {
                                'title': get_result[6]['HKD'][0],
                                "image_url": 'http://blog.buyforexonline.com/wp-content/uploads/2016/07/23463208_s-1.jpg',
                                'subtitle': 'Mua: ' + str(get_result[6]['HKD'][1]) +' |' + ' Bán: ' + str(
                                    get_result[6]['HKD'][3])
                            },
                            {
                                'title': get_result[16]['SGD'][0],
                                "image_url": 'http://blog.buyforexonline.com/wp-content/uploads/2016/07/23463208_s-1.jpg',
                                'subtitle': 'Mua: ' + str(get_result[16]['SGD'][1]) +' |' + ' Bán: ' + str(
                                    get_result[16]['SGD'][3])
                            },
                            {
                                'title': get_result[17]['THB'][0],
                                "image_url": 'http://blog.buyforexonline.com/wp-content/uploads/2016/07/23463208_s-1.jpg',
                                'subtitle': 'Mua: ' + str(get_result[17]['THB'][1]) +' |' + ' Bán: ' + str(
                                    get_result[17]['THB'][3])
                            }
                        ]
                    }
                }
            }
        ]
    }
    return json_result
