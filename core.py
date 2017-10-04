#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import requests
import random
from bs4 import BeautifulSoup as Parser
import json

def get_pic(keyword):
    url1 = 'https://www.pexels.com/search/' + keyword + '/'
    page = requests.get(url1)
    html = Parser(page.text, "html.parser")
    compressed = []
    fullsize = []
    for link in html.find('div', {'class': 'photos'}).find_all('a'):
        fullsize.append(link.get('href'))
    for link in html.find('div', {'class': 'photos'}).find_all('img'):
        compressed.append(link.get('src'))

    del page
    del html

    rannum = random.randint(0, len(compressed)-1)

    res1 = compressed[rannum]

    url2 = 'https://www.pexels.com/' + fullsize[rannum]
    pic = requests.get(url2)
    html2 = Parser(pic.text, "html.parser")
    res2 = html2.find('a', {'class': 'js-download'}).get('href')

    return res1, res2

def get_mus(keyword):
    url1 = 'http://ccmixter.org/api/query?f=json&score=4&t=links_stream&lic=by&rand=1&limit=20&tags=' + keyword
    page1 = requests.get(url1)
    mus_list = json.loads(page1.text)
    rannum = random.randint(0, len(mus_list)-1)
    res = mus_list[rannum]['files'][0]['download_url']
    return res
