import scrapy
import undetected_chromedriver as uc
import time
from random import randint
from random import uniform
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver


def links():
    options = uc.ChromeOptions()
    options.add_argument(
        '--user-data-dir=C:/Users/Andrei/AppData/Local/Google/Chrome/User Data/Default')
    driver = uc.Chrome(options=options)
    driver.get('https://nl.aliexpress.com/item/1005004527246828.html?spm=a2g0o.store_pc_allProduct.8148356.1.4dcd659dxwPDzm&pdp_npi=2%40dis%21USD%21US%20%24182.45%21US%20%24109.47%21%21%21%21%21%402103204216757963374578375e1442%2112000029481519906%21sh')

    time.sleep(uniform(1.5, 4.4))
    print("name: " + driver.find_element(By.CSS_SELECTOR,
                                         'div.product-title > h1').text)
    print("price: " + driver.find_element(By.CSS_SELECTOR,
                                          'div.product-price-current > span').text)
    print("image: " + driver.find_element(By.CSS_SELECTOR,
                                          'div.image-view-magnifier-wrap > img').get_attribute("src"))

    for i in range(10):
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
        time.sleep(uniform(0.2, 0.6))
    despription_box = driver.find_element(By.ID, 'product-description')
    boxes = despription_box.find_elements(By.CSS_SELECTOR, 'div')
    print(len(boxes))
    for box in boxes:
        try:
            if box.find_element(By.CSS_SELECTOR, 'div'):
                print('description : ' +
                      box.find_element(By.CSS_SELECTOR, 'div').text)
        except:
            continue

    driver.close()
