import scrapy
import json
from scrapy.http.response.html import HtmlResponse
from demo.items import DemoItem


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

    def parse(self, response: HtmlResponse):
        # 提取首页所有名言，保存至变量mingyan
        mingyan = response.css('div.quote')
        # 下一页
        next_page = response.css("ol.page-navigator li.next a::attr(href)").extract_first()
        for item in mingyan:
            json_data = dict()
            title = item.css(".text::text").extract_first()
            author = item.css(".author::text").extract_first()
            tags = item.css('.tags .tag::text').extract()  # 提取标签
            detail = item.css("span>a::attr(href)").extract_first()  # 提取详情地址
            data_item = DemoItem(title=title, author=author, tags=tags, detail=detail)

            # yield data_item
            # 获取图片地址--response.follow 追踪链接，如：取得的连接是/static/index 这样的 使用follow 会自动加上当前域名
            # 注意 这里 yield  因为有多层页面抓取数据  这里将数据传递出去 持续拼接
            yield response.follow(detail, callback=self.parse_src, meta={'item': data_item})

        if next_page is not None:
            # 注意这个yield 不加的话 爬虫 执行不下去 ，一次之后就关闭了，或许 这框架调用的是next()
            yield response.follow(next_page, callback=self.parse)

        # # 注意 windows下 文件编码是GBK  这里要指定打开编码
        # with open("data.json", "w+", encoding='utf-8') as f:
        #     s = json.dumps(self.data, ensure_ascii=False)
        #     f.write(s)
        # # 注意这里不能选择 追加模式
        # with open("src.json", "w+", encoding="utf-8") as f:
        #     f.write(json.dumps(self.src_data, ensure_ascii=False))

    """讲详情里面的图片保存下来"""

    def parse_src(self, response: HtmlResponse):
        # 获取上层页面抓取的数据
        item = response.meta['item']
        content = response.xpath('//div[@class="post-content"]//img/@src').extract()
        item['src'] = content
        yield item
