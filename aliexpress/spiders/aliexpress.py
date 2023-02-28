import scrapy
import undetected_chromedriver as uc
import time
from random import randint
from random import uniform
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
with open('C:/Users/Andrei/Desktop/python/aliexpress/links.txt', 'r') as f:
    links = [line.strip() for line in f]
# fmt: off
class AliexpressSpider(scrapy.Spider):
    name = 'aliexpress'
    start_urls = links
    custom_settings = { 
        "FEEDS" : {
        "/Users/Andrei/Desktop/python/aliexpress/sada.csv"
        : {"format": 
        "csv"
        }
    }}
 # fmt: 



    def parse(self, response):
        options = uc.ChromeOptions()
        options.add_argument(
            '--user-data-dir=C:/Users/Andrei/AppData/Local/Google/Chrome/User Data/Default')
        driver = uc.Chrome(options=options)
        driver.get(response.request.url)

        time.sleep(uniform(1.5, 4.4))
        items = {
            "name": driver.find_element(By.CSS_SELECTOR,
                                        'div.product-title > h1').text,
            "price": driver.find_element(By.CSS_SELECTOR,
                                         'div.product-price-current > span').text,
            "image":  driver.find_element(By.CSS_SELECTOR,
                                          'div.image-view-magnifier-wrap > img').get_attribute("src"),
            "description": [],
            "link": response.request.url,
        }

        for i in range(10):
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
            time.sleep(uniform(0.2, 0.6))
        despription_box = driver.find_element(By.ID, 'product-description')
        boxes = despription_box.find_elements(By.CSS_SELECTOR, 'div')
        print(len(boxes))
        for box in boxes:
            try:
                if box.find_element(By.CSS_SELECTOR, 'div'):
                    items['description'].append(
                        box.find_element(By.CSS_SELECTOR, 'div').text)

            except:
                continue
        yield items

        driver.quit()
