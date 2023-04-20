import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
import tldextract
import requests


class WebCrawler(scrapy.Spider):
    def __init__(self, url, url_list, es_interactor, *args, **kwargs):
        self.name = 'web_crawler'
        self.url = url
        self.url_list = url_list
        self.url_list.append(self.url)
        extracted = tldextract.extract(self.url)
        self.link_extractor = LinkExtractor()
        self.es_interactor = es_interactor
        self.allowed_domains = [extracted.registered_domain]
        super().__init__(*args, **kwargs)


    def start_requests(self):
        yield scrapy.Request(self.url, callback=self.parse)


    def parse(self, response, **kwargs):
        req = {"original_url": response.url, "text": response.text}
        resp = requests.post(self.es_interactor, json=req)
        self.url_list.append(response.url)
        if len(self.url_list) > 20:
            return
        for link in self.link_extractor.extract_links(response):
            if len(self.url_list) < 20:
                self.url_list.append(link.url)
                yield Request(link.url, callback=self.parse)
