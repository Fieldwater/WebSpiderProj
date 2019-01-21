# -*- coding: utf-8 -*-
import scrapy
import re

class RenrenSpider(scrapy.Spider):
    name = 'renren'
    allowed_domains = ['renren.com']
    start_urls = ['http://www.renren.com/744056789/profile']

    def start_requests(self):
        cookies = "anonymid=jos0yf236gj82e; depovince=BJ; jebecookies=930e6848-c762-4e85-87ff-f2c40bac8150|||||; _r01_=1; ick_login=a9d37db4-0961-4c24-8d5f-93d74d0180ef; _ga=GA1.2.1272571538.1547865515; _gid=GA1.2.1142613886.1547865515; _de=8E866BEAC73F5398E2A69D838E8B6F33696BF75400CE19CC; p=2d79e769383c472cd8b81cb76a3a16e29; first_login_flag=1; ln_uact=346605799@qq.com; ln_hurl=http://head.xiaonei.com/photos/0/0/men_main.gif; t=bdd4dd98c07727742ca64b2a69ed49fe9; societyguester=bdd4dd98c07727742ca64b2a69ed49fe9; id=744056789; xnsid=9c0650f5; ver=7.0; loginfrom=null; JSESSIONID=abcym5yJ3oweEcf6A_JHw; wp_fold=0; XNESSESSIONID=79f54e944eca; l4pager=0"
        cookies = {i.split('=')[0]:i.split('=')[1] for i in cookies.split('; ')}
        yield scrapy.Request(
            self.start_urls[0],
            callback=self.parse,
            cookies=cookies
        )

    def parse(self, response):
        print(re.findall('田园', response.body.decode()))

        yield scrapy.Request(
            "http://www.renren.com/744056789/profile?v=info_timeline",
            callback=self.parse_detail
        )

    def parse_detail(self,response):
        print(re.findall('田园', response.body.decode()))
