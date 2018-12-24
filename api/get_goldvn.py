# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re


def remove_tags(text):
    tag_re = re.compile(r'<[^>]+>')
    return tag_re.sub('', str(text))


def get_goldvn():
    url = 'https://www.24h.com.vn/'
    link = 'https://www.24h.com.vn/ttcb/giavang/giavang.php'
    req = requests.get(link)
    soup = BeautifulSoup(req.text, 'html.parser')
    img_url = 'https://cms-img.coverfox.com/gold-rate-in-india.jpg'
    # Resolving uptime
    uptime = []
    datetime = soup.find('div', class_='capNhat').find('span')
    for i in datetime:
        uptime.append(i)
    update_time = {
        'time': remove_tags(uptime[1]),
        'date': remove_tags(uptime[3])
    }
    # Resolving table goldvn
    table_golds = soup.find('div', id='div_ban_tin_gia_vang_2').find('table').find_all('span')[2:]
    table_gold = []
    for i in table_golds:
        for j in i:
            table_gold.append(str(j))
    nameGolds = []
    giaMua = []
    giaBan = []
    for i in range(0, 26, 3):
        nameGolds.append(table_gold[i])
    for i in range(1, 26, 3):
        giaMua.append(table_gold[i])
    for i in range(2, 27, 3):
        giaBan.append(table_gold[i])
    # Adding dict
    item = {
        'tenVang': nameGolds,
        'giaMua': giaMua,
        'giaBan': giaBan
    }
    # Adding result
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
                                'title': item['tenVang'][0],
                                'image_url': img_url,
                                'subtitle': 'Giá mua: ' + item['giaMua'][0] + ' | ' + 'Giá bán: ' + item['giaBan'][0],
                                'buttons': [
                                    {
                                        'type': 'web_url',
                                        'url': url,
                                        'title': 'Cập nhật lúc: ' + str(update_time['time'])
                                    }
                                ]
                            },
                            {
                                'title': item['tenVang'][1],
                                'image_url': img_url,
                                'subtitle': 'Giá mua: ' + item['giaMua'][1] + ' | ' + 'Giá bán: ' + item['giaBan'][1],
                                'buttons': [
                                    {
                                        'type': 'web_url',
                                        'url': url,
                                        'title': 'Cập nhật lúc: ' + str(update_time['time'])
                                    }
                                ]
                            },
                            {
                                'title': item['tenVang'][2],
                                'image_url': img_url,
                                'subtitle': 'Giá mua: ' + item['giaMua'][2] + ' | ' + 'Giá bán: ' + item['giaBan'][2],
                                'buttons': [
                                    {
                                        'type': 'web_url',
                                        'url': url,
                                        'title': 'Cập nhật lúc: ' + str(update_time['time'])
                                    }
                                ]
                            },
                            {
                                'title': item['tenVang'][3],
                                'image_url': img_url,
                                'subtitle': 'Giá mua: ' + item['giaMua'][3] + ' | ' + 'Giá bán: ' + item['giaBan'][3],
                                'buttons': [
                                    {
                                        'type': 'web_url',
                                        'url': url,
                                        'title': 'Cập nhật lúc: ' + str(update_time['time'])
                                    }
                                ]
                            },
                            {
                                'title': item['tenVang'][4],
                                'image_url': img_url,
                                'subtitle': 'Giá mua: ' + item['giaMua'][4] + ' | ' + 'Giá bán: ' + item['giaBan'][4],
                                'buttons': [
                                    {
                                        'type': 'web_url',
                                        'url': url,
                                        'title': 'Cập nhật lúc: ' + str(update_time['time'])
                                    }
                                ]
                            },
                            {
                                'title': item['tenVang'][5],
                                'image_url': img_url,
                                'subtitle': 'Giá mua: ' + item['giaMua'][5] + ' | ' + 'Giá bán: ' + item['giaBan'][5],
                                'buttons': [
                                    {
                                        'type': 'web_url',
                                        'url': url,
                                        'title': 'Cập nhật lúc: ' + str(update_time['time'])
                                    }
                                ]
                            },
                            {
                                'title': item['tenVang'][6],
                                'image_url': img_url,
                                'subtitle': 'Giá mua: ' + item['giaMua'][6] + ' | ' + 'Giá bán: ' + item['giaBan'][6],
                                'buttons': [
                                    {
                                        'type': 'web_url',
                                        'url': url,
                                        'title': 'Cập nhật lúc: ' + str(update_time['time'])
                                    }
                                ]
                            },
                            {
                                'title': item['tenVang'][7],
                                'image_url': img_url,
                                'subtitle': 'Giá mua: ' + item['giaMua'][7] + ' | ' + 'Giá bán: ' + item['giaBan'][7],
                                'buttons': [
                                    {
                                        'type': 'web_url',
                                        'url': url,
                                        'title': 'Cập nhật lúc: ' + str(update_time['time'])
                                    }
                                ]
                            },
                            {
                                'title': item['tenVang'][8],
                                'image_url': img_url,
                                'subtitle': 'Giá mua: ' + item['giaMua'][8] + ' | ' + 'Giá bán: ' + item['giaBan'][8],
                                'buttons': [
                                    {
                                        'type': 'web_url',
                                        'url': url,
                                        'title': 'Cập nhật lúc: ' + str(update_time['time'])
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
