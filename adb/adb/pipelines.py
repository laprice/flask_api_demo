from items import Product
from adb import settings
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.exceptions import DropItem
from scrapy.contrib.exporter import JsonLinesItemExporter
import datetime

class AdbPipeline(object):
    def __init__(self):
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.files = {}
        self.seen = set([])

    def spider_opened(self, spider):
        file = open('%s/%s/%s.json'% (settings.DATA_DIR,
                                      spider.name,
                                      datetime.date.today().isoformat()),
                    'w+b')
        self.files[spider] = file
        self.exporter = JsonLinesItemExporter(file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        if self.seen_before(item):
            raise DropItem
        self.exporter.export_item(item)
        return item

    def seen_before(self, item):
        if item['product'] in self.seen:
            return True
        else:
            self.seen.add(item['product'])
            return False
