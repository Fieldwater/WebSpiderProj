# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
import json
import urllib

class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com', 'p.3.cn']
    start_urls = ["https://book.jd.com/booksort.html"]

    def parse(self, response):
        # big category list
        dt_list = response.xpath("//div[@class='mc']/dl/dt")
        for dt in dt_list:
            item = {}
            item["main_cat"] = dt.xpath("./a/text()").extract_first()
            em_list = dt.xpath("./following-sibling::dd[1]/em")
            for em in em_list:
                item["sec_cat"] = em.xpath("./a/text()").extract_first()
                item["sec_href"] = em.xpath("./a/@href").extract_first()
                if item["sec_href"] is not None:
                    item["sec_href"] = "https:" + item["sec_href"]
                    yield scrapy.Request(
                        item["sec_href"],
                        callback=self.parse_book_list,
                        meta={"item": deepcopy(item)}
                    )

    def parse_book_list(self, response):
        item = response.meta["item"]
        li_list = response.xpath("//div[@id='plist']//li")
        for li in li_list:
            item["book_img"] = li.xpath(".//div[@class='p-img']//img/@src").extract_first()
            if item["book_img"] is None:
                item["book_img"] = li.xpath(".//div[@class='p-img']//img/@data-lazy-img").extract_first()
            item["book_name"] = li.xpath(".//div[@class='p-name']//em/text()").extract_first().strip()
            item["book_author"] = li.xpath(".//div[@class='p-bookdetails']//span[@class='author_type_1']/a/text()").extract()
            item["book_press"] = li.xpath(".//div[@class='p-bookdetails']/span[@class='p-bi-store']/a/text()").extract_first()
            item["book_publish_date"] = li.xpath(".//div[@class='p-bookdetails']/span[@class='p-bi-date']/text()").extract_first().strip()
            item["book_sku"] = li.xpath("./div[@class='gl-i-wrap j-sku-item']/@data-sku").extract_first()

            if item["book_img"] is not None:
                item["book_img"] = "https:" + item["book_img"]

            yield scrapy.Request(
                "https://p.3.cn/prices/mgets?&skuIds=J_{}".format(item["book_sku"]),
                callback=self.parse_book_price,
                meta={"item": deepcopy(item)}
            )

        # 翻页
        next_url = response.xpath("//a[@class='pn-next']/@href").extract_first()
        if next_url is not None:
            next_url = urllib.parse.urljoin(response.url, next_url)
            yield scrapy.Request(
                next_url,
                callback=self.parse_book_list,
                meta = {"item": deepcopy(item)}
            )

    def parse_book_price(self, response):
        item = response.meta["item"]
        item["book_price"] = json.loads(response.body.decode())[0]["op"]
        print(item)


