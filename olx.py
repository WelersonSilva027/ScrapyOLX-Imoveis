#USER AGENT
#Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36
"""
import requests

r = requests.get('https://www.olx.com.br/imoveis', headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'})

r.text

from parsel import Selector
s = Selector(text=r.text)

s.xpath('//script[@id="__NEXT_DATA__"]/text()')

import json

html = json.loads(s.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
)

houses = html.get('props').get('pageProps').get('ads')
"""
from typing import Iterable
import scrapy
import json

from scrapy.http import Response

class OlxHouses(scrapy.Spider):
    name = 'olx'

    custom_settings = {
        'USER_AGENT' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'AUTOTHROTTLE_ENABLE': True,
        'AUTOTHROTTLE_START_DELAY' : 15,
    }

    def start_requests(self):
        yield scrapy.Request('https://www.olx.com.br/imoveis')
    
    def parse(self, response, **kwargs):
        html = json.loads(response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
)
        houses =  html.get('props').get('pageProps').get('ads')

        for house in houses:
            yield{
                'title' : house.get('title'),
                'price' : house.get('price'),
                'locations' : house.get('location')
            }
