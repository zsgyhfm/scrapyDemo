import scrapy
import json


class FirstSpider(scrapy.Spider):
    name = "First_spider"
    # start_urls = ['http://lab.scrapyd.cn']  等同于下面的start_requests方法
    data = []

    def start_requests(self):
        urls = [
            'http://lab.scrapyd.cn'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # 提取首页所有名言，保存至变量mingyan
        mingyan = response.css('div.quote')
        # 下一页
        next_page = response.css("ol.page-navigator li.next a::attr(href)").extract_first()
        for item in mingyan:
            json_data = dict()
            json_data["title"] = item.css(".text::text").extract_first()
            json_data["author "] = item.css(".author::text").extract_first()
            json_data['tags'] = item.css('.tags .tag::text').extract()  # 提取标签
            self.data.append(json_data)

        if next_page is not None:
            print("*" * 50)
            print("执行下一页")
            print("*" * 50)
            # 注意这个yield 不加的话 爬虫 执行不下去 ，一次之后就关闭了，或许 这框架调用的是next()
            yield response.follow(next_page, callback=self.parse)
        # 注意 windows下 文件编码是GBK  这里要指定打开编码
        with open("data.json", "w+", encoding='utf-8') as f:
            s = json.dumps(self.data, ensure_ascii=False)
            f.write(s)
