import requests

def get_weather(city):
    url = 'http://api.apixu.com/v1/current.json?key=94aad9f1dddb4e9c89673931182211&q=' + str(city) + '&lang=vi'
    req = requests.get(url)
    p = req.json()
    json_result = {
        'set_attributes': {
            'temp_c': p['current']['temp_c'],
            'text': p['current']['condition']['text'],
            'humidity': p['current']['humidity']
        },
        'messages': []
    }
    return json_result
if __name__ == '__main__':
    get_weather('Ho chi minh city')