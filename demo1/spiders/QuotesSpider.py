import scrapy


class QuotesSpider(scrapy.Spider):
    # 唯一的标识
    name = "QuotesSpider"

    def start_requests(self):
        # 爬虫起始的url
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]

        for url in urls:
            # 将url传递给request  并调用parse函数进行解析
            yield scrapy.Request(url=url, callback=self.parse())

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
