# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy import signals
from scrapy.contrib.exporter import JsonItemExporter

class GamesscorePipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.file = open('items.json', 'wb')
        self.exporter = JsonItemExporter(self.file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.checkData(item, "title")
        self.checkData(item, "summary")
        self.checkData(item, "cover_image")
        self.checkData(item, "score")

        self.exporter.export_item(item)

        return item

    def checkData(self, item, field):
        if len(item[field]) > 0:
            newText = item[field][0].encode("utf-8")
            item[field] = newText.strip()
        else:
            item[field] = ""
