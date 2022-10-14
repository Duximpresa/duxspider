import scrapy
from scrapy import Request


class BqbHotSpider(scrapy.Spider):
    name = 'bqb_hot'
    allowed_domains = ['fabiaoqing.com']
    start_urls = ['https://fabiaoqing.com/bqb/lists/type/hot/page/1.html']

    def start_requests(self):
        for i in range(1, 51):
            url = f"https://fabiaoqing.com/bqb/lists/type/hot/page/{i}.html"
            yield Request(url)

    def parse(self, resp, **kwargs):
        # print("====>", resp)
        hrefs = resp.xpath("//div[@id='container']/div/div/a/@href").extract()[:-1]
        for href in hrefs:
            href = resp.urljoin(href)
            yield Request(href, callback=self.parse2)
            # break

    def parse2(self, resp, **kwargs):
        title = resp.xpath("//h1[@class='ui header']/text()").extract_first()
        img_srcs = resp.xpath("//div[@class='bqppdiv1']/img/@data-original").extract()
        img_titles = resp.xpath("//div[@class='bqppdiv1']/img/@title").extract()
        img = zip(img_titles, img_srcs)
        yield {
            "title": title,
            "img": img
        }

