import requests
import re
import json
def remove_tags(text):
    tag_re = re.compile(r'<[^>]+>')
    return tag_re.sub('', str(text))

def get_news_amway():
    headurl = 'http://www.amwaytoday.com.vn'
    url = 'http://www.amwaytoday.com.vn/news.amway.article.grid.json?fbclid=IwAR1l1yqIZwmA-B2y21YdZZ-PA73alqWgdzYQEMOyQsX9sYhZIOYgcb56nLs'
    req = requests.get(url)
    data_news = req.json()
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
                                'title': data_news['articles'][0]['title'],
                                'image_url': headurl + data_news['articles'][0]['imageLink'],
                                'subtitle': 'Nguồn: www.amwaytoday.com.vn',
                                'buttons': [
                                    {
                                        'type': 'web_url',
                                        'url': headurl + data_news['articles'][0]['link'],
                                        'title': 'Xem'
                                    }
                                ]
                            },
                            {
                                'title': data_news['articles'][1]['title'],
                                'image_url': headurl + data_news['articles'][1]['imageLink'],
                                'subtitle': 'Nguồn: www.amwaytoday.com.vn',
                                'buttons': [
                                    {
                                        'type': 'web_url',
                                        'url': headurl + data_news['articles'][1]['link'],
                                        'title': 'Xem'
                                    }
                                ]
                            },
                            {
                                'title': data_news['articles'][2]['title'],
                                'image_url': headurl + data_news['articles'][2]['imageLink'],
                                'subtitle': 'Nguồn: www.amwaytoday.com.vn',
                                'buttons': [
                                    {
                                        'type': 'web_url',
                                        'url': headurl + data_news['articles'][2]['link'],
                                        'title': 'Xem'
                                    }
                                ]
                            },
                            {
                                'title': data_news['articles'][3]['title'],
                                'image_url': headurl + data_news['articles'][3]['imageLink'],
                                'subtitle': 'Nguồn: www.amwaytoday.com.vn',
                                'buttons': [
                                    {
                                        'type': 'web_url',
                                        'url': headurl + data_news['articles'][3]['link'],
                                        'title': 'Xem'
                                    }
                                ]
                            },
                            {
                                'title': data_news['articles'][4]['title'],
                                'image_url': headurl + data_news['articles'][4]['imageLink'],
                                'subtitle': 'Nguồn: www.amwaytoday.com.vn',
                                'buttons': [
                                    {
                                        'type': 'web_url',
                                        'url': headurl + data_news['articles'][4]['link'],
                                        'title': 'Xem'
                                    }
                                ]
                            },
                            {
                                'title': data_news['articles'][5]['title'],
                                'image_url': headurl + data_news['articles'][5]['imageLink'],
                                'subtitle': 'Nguồn: www.amwaytoday.com.vn',
                                'buttons': [
                                    {
                                        'type': 'web_url',
                                        'url': headurl + data_news['articles'][5]['link'],
                                        'title': 'Xem'
                                    }
                                ]
                            },
                            {
                                'title': data_news['articles'][6]['title'],
                                'image_url': headurl + data_news['articles'][6]['imageLink'],
                                'subtitle': 'Nguồn: www.amwaytoday.com.vn',
                                'buttons': [
                                    {
                                        'type': 'web_url',
                                        'url': headurl + data_news['articles'][6]['link'],
                                        'title': 'Xem'
                                    }
                                ]
                            },
                            {
                                'title': data_news['articles'][7]['title'],
                                'image_url': headurl + data_news['articles'][7]['imageLink'],
                                'subtitle': 'Nguồn: www.amwaytoday.com.vn',
                                'buttons': [
                                    {
                                        'type': 'web_url',
                                        'url': headurl + data_news['articles'][7]['link'],
                                        'title': 'Xem'
                                    }
                                ]
                            },
                            {
                                'title': data_news['articles'][8]['title'],
                                'image_url': headurl + data_news['articles'][8]['imageLink'],
                                'subtitle': 'Nguồn: www.amwaytoday.com.vn',
                                'buttons': [
                                    {
                                        'type': 'web_url',
                                        'url': headurl + data_news['articles'][8]['link'],
                                        'title': 'Xem'
                                    }
                                ]
                            }

                        ]
                    }
                }
            }
        ]
    }
    return json_result