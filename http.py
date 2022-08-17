"""This module contains the ``SeleniumRequest`` class"""

from scrapy import Request


class SeleniumRequest(Request):
    """Scrapy ``Request`` subclass providing additional arguments"""

    def __init__(self, 
        # wait_time=None, wait_until=None, screenshot=False, script=None, 
        *args, **kwargs):
        
        # self.wait_time = wait_time
        # self.wait_until = wait_until
        # self.screenshot = screenshot
        # self.script = script

        super().__init__(*args, **kwargs)


    def spider_opened(self, spider):
        print('Spider opened: %s' % spider.name)