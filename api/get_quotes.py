# -*- coding: utf8 -*-
import requests
from bs4 import BeautifulSoup
import re
import random

def remove_tags(text):
    tag_re = re.compile(r'<[^>]+>')
    return tag_re.sub('', str(text))
def remove_number(text):
    number = re.compile(r'^[\d]+\.?.')
    return number.sub('', str(text))

def get_quote_1():
    link = 'https://trithucvn.net/doi-song/100-cau-trich-dan-cua-nhung-nguoi-thanh-cong-nhat-the-gioi-p-1.html'
    req = requests.get(link)
    soup = BeautifulSoup(req.text, 'html.parser')
    text = soup.find('div', class_ = 'entry').find_all('p')
    quotes_list = []
    for i in text:
        for j in i:
            c = remove_tags(j)
            matched = re.search(r'[\d]+\..+', str(c))
            if matched:
                quotes_list.append(matched.group())
                break
    return quotes_list

def get_quote_2():
    link = 'https://ocuaso.com/stt-danh-ngon/stt-thanh-cong-danh-ngon-101-cau-noi-hay-ve-su-thanh-cong-hay.html'
    req = requests.get(link)
    soup = BeautifulSoup(req.text, 'html.parser')
    text = soup.find('div', id= 'ftwp-postcontent').find_all('p')
    quotes_list = []
    for i in text:
        matched = re.search(r'[\d]+\,.+',str(remove_tags(i)))
        if matched:
            quotes_list.append(matched.group())
    return quotes_list
def get_quotes():
    quote1 = []
    for i in get_quote_1():
        c = remove_number(i)
        quote1.append(c)
    quote2 = []
    for i in get_quote_2():
        c = remove_number(i)
        quote2.append(c)
    all_quotes = quote1 + quote2
    img = [
        'https://blog.ipleaders.in/wp-content/uploads/2018/01/BV-Acharya-5.jpg',
        'http://myocn.net/wp-content/uploads/2018/04/Gospel.jpg',
        'https://cdn.pixabay.com/photo/2016/04/27/04/48/silhouette-1355969_960_720.jpg',
        'https://content.thriveglobal.com/wp-content/uploads/2017/12/517128288.jpg',
        'https://mensagensereflexoes.com.br/wp-content/uploads/2017/12/ser-forte.png',
        'http://www.hippocampus.io/wp-content/uploads/2018/06/01.06.2018-photo-for-blog-post-18.jpg',
        'https://radiofacts.com/wp-content/uploads/2016/02/o-SECRETS-OF-SUCCESS-facebook.jpg',
        'https://steemitimages.com/DQmNiLHSVVLYKoTFJy8uf3nuGgLJKGhtuFey4hegAtgEywZ/obstacles-to-success.jpg',
        'https://cdn.lifehack.org/wp-content/uploads/2016/05/23041155/success-mindset.jpeg',
        'https://cdns.klimg.com/merdeka.com/i/w/news/2017/09/25/890483/670x335/terungkap-ini-5-rahasia-orang-sukses-dunia.jpg'
    ]
    json_result = {
        'messages': [
            {'text': random.choice(all_quotes)},
            {
                'attachment': {
                    'type': 'image',
                    'payload': {
                        'url': random.choice(img)
                    }
                }
            }
        ]
    }
    return json_result
