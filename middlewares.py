"""This module contains the ``SeleniumMiddleware`` scrapy middleware"""

from importlib import import_module

from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.http import HtmlResponse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from .http import SeleniumRequest

from selenium import webdriver##

class SeleniumMiddleware:
    """Scrapy middleware handling the requests using selenium"""

    def __init__(self, 
        wait_until='wait_until',
        # driver_name, 
        # driver_executable_path,
        # browser_executable_path, 
        # command_executor, 
        # driver_arguments
        ):

        self.driver = False
        
        # locally installed driver
        # default_options = webdriver.ChromeOptions()
        # default_options.add_argument('--disable-gpu')
        # default_options.add_argument("--headless")
        # default_options = default_options.to_capabilities()
        # driver = webdriver.Chrome(desired_capabilities=default_options)

        # self.driver = driver
        
    @classmethod
    def from_crawler(cls, crawler):
        """Initialize the middleware with the crawler settings"""
        middleware = cls()
        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
        return middleware

    def process_request(self, request, spider):
        """Process a request using the selenium driver if applicable"""
        if not isinstance(request, SeleniumRequest): #SeleniumRequest
            # print('no instance for SeleniumRequest')
            return None
        
        print('[middleware/SSeleniumMiddleware] : processing request', request.url, '...')

        default_options = webdriver.ChromeOptions()
        default_options.add_argument('--disable-gpu')
        default_options.add_argument("--headless")
        default_options = default_options.to_capabilities()
        driver = webdriver.Chrome(desired_capabilities=default_options)

        self.driver = driver
        self.driver.get(request.url)

        if not 'wait_until' in request.meta.keys():
            # print('NO wait_until')
            self.wait_until = False
        else :
            # print('YES waiting_until...')
            self.wait_until = EC.presence_of_element_located(
            (
            By.CSS_SELECTOR, 
            request.meta.get('wait_until')
            )) #ul.sidemenu-list.first-level >li >a

        if self.wait_until :
            WebDriverWait(self.driver, 2).until(self.wait_until)
            # print('did wait_until')
        else :
            WebDriverWait(self.driver, 4)
            # print('did not wait_until')

        for cookie_name, cookie_value in request.cookies.items():
            self.driver.add_cookie(
                {
                    'name': cookie_name,
                    'value': cookie_value
                }
            )

        body = str.encode(self.driver.page_source)

        # Expose the driver via the "meta" attribute
        request.meta.update({'driver': self.driver})

        # print('[middleware/SSeleniumMiddleware] :','returning response for', request.url)

        return HtmlResponse(
            self.driver.current_url,
            body=body,
            encoding='utf-8',
            request=request
        )

    def spider_closed(self):
        """Shutdown the driver when spider is closed"""
        # print('[middleware/SSeleniumMiddleware] : Spider driver closed')
        () if not self.driver else self.driver.quit()

    def spider_opened(self, spider):
        print('Spider opened: %s' % spider.name)