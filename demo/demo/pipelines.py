# -*- coding: utf-8 -*-

# Define your item pipelines here
# 需要在setting里面配置ITEM_PIPELINES
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
# 两者的区别  前者是一起写入 ，后者每次收到item处理后就写入，如果抓取内容大 就选择后者
from scrapy.exporters import JsonItemExporter,JsonLinesItemExporter


# class DemoPipeline(object):
#     def __init__(self):
#         """这里打开文件 """
#         self.fp = open("data.json", "w", encoding="utf-8")
#
#     def process_item(self, item, spider):
#         """接收从spider 来的item数据 进行保存 操作-当有item过来的时候会调用"""
#         self.fp.write(json.dumps(item.__dict__,ensure_ascii=False)+",")
#         return item
#
#     def open_spider(self, spider):
#         print("爬虫开始的时候调用")
#
#     def close_spider(self, spider):
#         print("爬虫结束 调用")
#         self.fp.close()


class DemoPipeline(object):
    def __init__(self):
        """这里打开文件 """
        self.fp = open("data.json", "wb")
        self.exporter = JsonItemExporter(self.fp, encoding="utf-8", ensure_ascii=False)

    def process_item(self, item, spider):
        """接收从spider 来的item数据 进行保存 操作-当有item过来的时候会调用"""
        self.exporter.export_item(item)
        return item

    def open_spider(self, spider):
        self.exporter.start_exporting()
        print("爬虫开始的时候调用")

    def close_spider(self, spider):
        print("爬虫结束 调用")
        self.exporter.finish_exporting()
        self.fp.close()

#
# class DemoPipeline(object):
#     def __init__(self):
#         """这里打开文件 """
#         self.fp = open("data.json", "wb")
#         self.exporter = JsonLinesItemExporter(self.fp, encoding="utf-8", ensure_ascii=False)
#
#     def process_item(self, item, spider):
#         """接收从spider 来的item数据 进行保存 操作-当有item过来的时候会调用"""
#         print("当前爬虫是:",spider.name)
#         self.exporter.export_item(item)
#         #  一定要return 因为还可能有其他处理函数使用这个item
#         return item
#
#     def open_spider(self, spider):
#         self.exporter.start_exporting()
#         print("爬虫开始的时候调用")
#
#     def close_spider(self, spider):
#         print("爬虫结束 调用")
#         self.fp.close()