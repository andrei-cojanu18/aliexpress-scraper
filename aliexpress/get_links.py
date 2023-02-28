import undetected_chromedriver as uc
import time
from random import randint
from random import uniform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver


def load_dynamic_site(url):
    options = webdriver.ChromeOptions()
    options.add_argument(
        '--user-data-dir=C:/Users/Andrei/AppData/Local/Google/Chrome/User Data/Default')
    options.add_argument('proxy-server=82.196.11.105:1080')
    driver = uc.Chrome(options=options)
    driver.get(url)
    time.sleep(randint(1, 5))
    # for i in range(20):
    #     driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
    #     time.sleep(0.2)  # wait for 200 milliseconds
    # html = driver.page_source
    # with open("C:/Users/Andrei/idk/idk/page_source.txt", "w", encoding="utf-8") as file:
    #     file.write(driver.page_source)
    # print(html)
    boxes = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.module.m-o.m-o-large-all-detail > div > div > ul > li')))
    count = 0
    links = []
    for box in boxes:
        time.sleep(uniform(0.2, 0.6))
        links.append(box.find_element(By.CSS_SELECTOR,
                     'div.detail > h3 > a').get_attribute("href"))
    print(len(links))

    driver.close()
    return links


if __name__ == "__main__":
    url = "https://nl.aliexpress.com/store/912161326/search/1.html?spm=a2g0o.store_pc_allProduct.8148361.2.45471dc9CyRGUT&origin=n&SortType=bestmatch_sort"
    links = load_dynamic_site(url)
    with open(r"C:/Users/Andrei/Desktop/ANDREI/aliexpress/aliexpress/spiders/links.txt", "w", encoding="utf-8") as file:
        for link in links:
            file.write(link + '\n')
