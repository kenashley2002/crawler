# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re

def remove_tags(text):
    tag_re = re.compile(r'<[^>]+>')
    return tag_re.sub('', str(text))

def get_oilrate(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    oil = soup.find('div', class_ = 'list-table').find_all('div')
    xang_95_4 = [remove_tags(oil[5]), remove_tags(oil[6])]
    xang_95_3 = [remove_tags(oil[9]), remove_tags(oil[10])]
    xang_E5_92 = [remove_tags(oil[13]), remove_tags(oil[14])]
    dau_do_1SV = [remove_tags(oil[17]), remove_tags(oil[18])]
    dau_do_5S = [remove_tags(oil[21]), remove_tags(oil[22])]
    dau_hoa = [remove_tags(oil[25]), remove_tags(oil[26])]
    json_result = {
        'messages': [{
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'generic',
                    'image_aspect_ratio': 'square',
                    'elements': [
                        {
                            'title': 'Xăng RON 95-IV',
                            'img_url': 'https://investorplace.com/wp-content/uploads/2011/07/oil_chart_630_iStockphoto.jpg',
                            'subtitle': 'Vùng 1: '+ str(xang_95_4[0]) + ' | ' + 'Vùng 2: ' + str(xang_95_4[1])
                        },
                        {
                            'title': 'Xăng RON 95-III',
                            'img_url': 'https://investorplace.com/wp-content/uploads/2011/07/oil_chart_630_iStockphoto.jpg',
                            'subtitle': 'Vùng 1: ' + str(xang_95_3[0]) + ' | ' + 'Vùng 2: ' + str(xang_95_3[1])
                        },
                        {
                            'title': 'E5 RON 92-II',
                            'img_url': 'https://investorplace.com/wp-content/uploads/2011/07/oil_chart_630_iStockphoto.jpg',
                            'subtitle': 'Vùng 1: ' + str(xang_E5_92[0]) + ' | ' + 'Vùng 2: ' + str(xang_E5_92[1])
                        },
                        {
                            'title': 'DO 0,001S-V',
                            'img_url': 'https://investorplace.com/wp-content/uploads/2011/07/oil_chart_630_iStockphoto.jpg',
                            'subtitle': 'Vùng 1: ' + str(dau_do_1SV[0]) + ' | ' + 'Vùng 2: ' + str(dau_do_1SV[1])
                        },
                        {
                            'title': 'DO 0,05S-II',
                            'img_url': '',
                            'subtitle': 'Vùng 1: ' + str(dau_do_5S[0]) + ' | ' + 'Vùng 2: ' + str(dau_do_5S[1])
                        },
                        {
                            'title': 'Dầu hỏa',
                            'img_url': '',
                            'subtitle': 'Vùng 1: ' + str(dau_hoa[0]) + ' | ' + 'Vùng 2: ' + str(dau_hoa[1])
                        }
                    ]
                }
            }

        }]
    }
    return json_result