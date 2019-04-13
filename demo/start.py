from scrapy import cmdline

"""
执行scrapy命令
"""
# 这里 指定的是spider的name
cmdline.execute("scrapy crawl First_spider".split(" "))
# 等价于 cmdline.execute(["scrapy", "crawl", "First_spider"])
