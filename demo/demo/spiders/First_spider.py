import scrapy
import json
from scrapy.http.response import Response


class FirstSpider(scrapy.Spider):
    name = "First_spider"
    # start_urls = ['http://lab.scrapyd.cn']  等同于下面的start_requests方法
    data = []
    src_data = []

    def start_requests(self):
        urls = [
            'http://lab.scrapyd.cn'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: Response):
        # 提取首页所有名言，保存至变量mingyan
        mingyan = response.css('div.quote')
        # 下一页
        next_page = response.css("ol.page-navigator li.next a::attr(href)").extract_first()
        for item in mingyan:
            json_data = dict()
            json_data["title"] = item.css(".text::text").extract_first()
            json_data["author "] = item.css(".author::text").extract_first()
            json_data['tags'] = item.css('.tags .tag::text').extract()  # 提取标签
            json_data["details"] = item.css("span>a::attr(href)").extract_first()  # 提取详情地址
            self.data.append(json_data)
            # 获取图片地址
            yield response.follow(json_data["details"], callback=self.parse_src)

        if next_page is not None:
            print("*" * 50)
            print("执行下一页")
            print("*" * 50)
            # 注意这个yield 不加的话 爬虫 执行不下去 ，一次之后就关闭了，或许 这框架调用的是next()
            yield response.follow(next_page, callback=self.parse)
        # 注意 windows下 文件编码是GBK  这里要指定打开编码
        with open("data.json", "w+", encoding='utf-8') as f:
            print("-" * 50)
            print("保存------地址")
            print("-" * 50)
            s = json.dumps(self.data, ensure_ascii=False)
            f.write(s)
        with open("src.json", "w+", encoding="utf-8") as f:
            print("+"*50)
            print("保存src地址")
            print("+" * 50)
            f.write(json.dumps(self.src_data, ensure_ascii=False))

        # 上面的数据保存完毕后 读取json_data 下载图片

    """讲详情里面的图片下载下来"""

    def parse_src(self, response: Response):
        content = response.xpath('//div[@class="post-content"]//img/@src').extract()
        for i in content:
            self.src_data.append({"src": i})
