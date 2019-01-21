# -*- coding: utf-8 -*-
import scrapy
import re

class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/login']

    # Remember to input password

    # # Method 1
    # def parse(self, response):
    #     authenticity_token = response.xpath("//input[@name='authenticity_token']/@value").extract_first()
    #     utf8 = response.xpath("//input[@name='utf8']/@value").extract_first()
    #     commit = response.xpath("//input[@name='commit']/@value").extract_first()
    #     post_data = dict(
    #         login = 'Fieldwater',
    #         password = '',
    #         authenticity_token=authenticity_token,
    #         utf8 = utf8,
    #         commit = commit
    #     )
    #     # send post request
    #     yield scrapy.FormRequest(
    #         "https://github.com/session",
    #         formdata=post_data,
    #         callback=self.after_login
    #
    #     )

    # Method 2 using scrapy.FormRequest.from_response
    def parse(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formdata={'login': 'Fieldwater', 'password': ''},
            callback=self.after_login
        )

    def after_login(self, response):
            with open('after_login2.html', 'w', encoding='utf-8') as f:
                f.write(response.body.decode())
            print(re.findall("Fieldwater", response.body.decode()))

