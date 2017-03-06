from scrapy.spiders import BaseSpider
from appScrapy.items import AppscrapyItem

class AppScrapy(BaseSpider):
    name = 'app_scrapy'
    start_urls = ["https://itunes.apple.com/cn/genre/ios-yu-le/id6016?mt=8"]

    def parse(self, response):
        result = []
        lis = response.xpath("//div[@class='grid3-column']/div")
        for li in lis:
            array = li.xpath("./ul/li")
            for node in array:
                item = AppscrapyItem()
                item["name"] = node.xpath("./a/text()").extract()
                item["url"] = node.xpath("./a/@href").extract()
                result.append(item)
        return result
