# -*- coding: utf-8 -*-
import scrapy
from Sunshine.items import SunshineItem

class SunshineSpider(scrapy.Spider):
    name = 'Sunshine'
    allowed_domains = ['sun0769.com']
    start_urls = ["http://wz.sun0769.com/index.php/question/questionType?type=4&page=0"]

    def parse(self, response):
        # 分组
        tr_list = response.xpath("//div[@class='greyframe']/table[2]/tr/td/table/tr")
        for tr in tr_list:
            item = SunshineItem()
            item["title"] = tr.xpath("./td[2]/a[@class='news14']/@title").extract_first()
            item["href"] = tr.xpath("./td[2]/a[@class='news14']/@href").extract_first()
            item["publish_date"] = tr.xpath("./td[@class='t12wh']/text()").extract_first()

            # 生成新的请求、meta实现不同函数中的参数传递
            yield scrapy.Request(
                item["href"],
                callback = self.parse_detail,
                meta = {"item": item, "count": count}
            )
        # 翻页，用文本内容定位
        # next_url = response.xpath("//a[text()='>']/@href").extract_first()
        # if next_url is not None:
        #     yield scrapy.Request(
        #         next_url,
        #         callback = self.parse
        #     )

    # 处理详情页
    def parse_detail(self, response):
                item = response.meta["item"]
                count = response.meta["count"]

                item["content_img"] = response.xpath("//div[@class='textpic']/img/@src").extract()

                if item["content_img"] == []:
                    item["content"] = response.xpath("//div[@class='wzy1']/table[2]/tr[1]/td[@class='txt16_3']/text()").extract()
                else:
                    item["content"] = response.xpath("//td[@class='txt16_3']/div[@class='contentext']/text()").extract()

                item["content_img"] = ["http://wz.sun0769.com" + i for i in item['content_img']]
                # print(item)
                # print(count)
                yield item