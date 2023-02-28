import scrapy
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import selenium


class ProccesoraltexSpider(scrapy.Spider):
    name = 'test'
    start_urls = ['https://altex.ro/procesoare-calculator/cpl/']




# fmt: off
    custom_settings = { 
        "FEEDS" : {
        "/Users/Andrei/Desktop/python/aliexpress/andreiesmek.csv"
        : {"format": 
        "csv"
        }
    }}
 # fmt: 



    def parse(self, response):

        nameh1 = response.css("ul.Products.flex.flex-wrap.relative.-mx-1.sm\:-mx-2 > li > a")
        for name in nameh1 :
            yield{
                "name": name.css("h2::text").get(),
            }
        pass
