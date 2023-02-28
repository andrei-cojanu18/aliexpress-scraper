import sys
import subprocess
import undetected_chromedriver as uc
import time
import re
import os
from random import randint
from random import uniform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor
from selenium.common.exceptions import NoSuchElementException
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QFileDialog, QMessageBox
from PyQt5 import uic, QtCore


class ScrapyGUI(QMainWindow):
    feeds_path = ''
    global_path = os.getcwd()
    logChanged = QtCore.pyqtSignal(str)
    started = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi("gui.ui", self)
        self._process = QtCore.QProcess(self)
        self._process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        self._process.setProgram('scrapy')
        self._process.started.connect(self.started)
        self._process.finished.connect(self.process_finished)
        self.show()

        self.GeneratLink_button.clicked.connect(self.TakeLink)
        self.browse_btn.clicked.connect(self.browse)
        self.ShopLink.textChanged.connect(self.text_changed)
        self.start_scrap_btn.clicked.connect(self.start_scrap)
        self.checkCsv.setChecked(True)

    def TakeLink(self):
        url = self.ShopLink.text()
        if "aliexpress" in url:
            options = webdriver.ChromeOptions()
            options.add_argument(
                '--user-data-dir=C:/AppData/Local/Google/Chrome/User Data/Default')
            options.add_argument('proxy-server=82.196.11.105:1080')
            driver = uc.Chrome(options=options)
            driver.get(url)
            time.sleep(randint(1, 5))

            boxes = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.module.m-o.m-o-large-all-detail > div > div > ul > li')))
            count = 0
            links = []
            for box in boxes:
                time.sleep(uniform(0.2, 0.6))
                links.append(box.find_element(By.CSS_SELECTOR,
                                              'div.detail > h3 > a').get_attribute("href"))
            print(len(links))

            pagination = True
            while pagination == True:
                try:
                    button = driver.find_element(
                        By.CSS_SELECTOR, "div.ui-pagination-navi.util-left > a.ui-pagination-next")
                except NoSuchElementException:
                    break

                button.click()

                time.sleep(randint(1, 5))
                driver.refresh()
                time.sleep(randint(1, 3))
                try:
                    boxes = WebDriverWait(driver, 5).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.module.m-o.m-o-large-all-detail > div > div > ul > li')))
                except:
                    driver.refresh()
                    time.sleep(randint(1, 3))
                    boxes = WebDriverWait(driver, 5).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.module.m-o.m-o-large-all-detail > div > div > ul > li')))

                for box in boxes:
                    time.sleep(uniform(0.1, 0.3))
                    links.append(box.find_element(By.CSS_SELECTOR,
                                                  'div.detail > h3 > a').get_attribute("href"))

            driver.close()
            with open(r"links.txt", "w", encoding="utf-8") as file:
                for link in links:
                    file.write(link + '\n')
            self.process_finished

        else:
            self.label.setText("This is not a aliexpress link")
            self.label.setStyleSheet(
                "color: red")

    def text_changed(self):
        if self.ShopLink.text():
            self.GeneratLink_button.setEnabled(True)
        else:
            self.GeneratLink_button.setEnabled(False)

    def browse(self):

        count = 0
        if self.checkCsv.isChecked() == True:
            fname = QFileDialog.getSaveFileName(
                self, "Select Folder", "", "CSV Files(*.csv)")
            with open(self.global_path.replace('\\', '/') + '/aliexpress/spiders/aliexpress.py') as f:
                lines = f.read().splitlines()
            with open(self.global_path.replace('\\', '/') + '/aliexpress/spiders/aliexpress.py', 'w') as f:
                count = 0
                for line in lines:
                    count += 1
                    if count == 19:
                        string = "csv"
                        f.write(re.sub(r'"[^]]*"', '"' +
                                string+'"', line) + "\n")
                    else:
                        f.write(line + '\n')
        elif self.checkJson.isChecked() == True:
            fname = QFileDialog.getSaveFileName(
                self, "Select Folder", "", "JSON Files(*.json)")
            with open(self.global_path.replace('\\', '/') + '/aliexpress/spiders/aliexpress.py') as f:
                lines = f.read().splitlines()
            with open(self.global_path.replace('\\', '/') + '/aliexpress/spiders/aliexpress.py', 'w') as f:
                count = 0
                for line in lines:
                    count += 1
                    if count == 19:
                        string = "json"
                        f.write(re.sub(r'"[^]]*"', '"' +
                                string+'"', line) + "\n")
                    else:
                        f.write(line + '\n')
        self.feeds_path = fname[0]
        self.label_2.setText("Path chosen")
        self.listWidget.clear()
        self.listWidget.insertItem(1, self.feeds_path)
        self.change_save_path()
        print(fname[0])

    def start_scrap(self):
        self._process.setWorkingDirectory(
            self.global_path.replace('\\', '/'))
        self._process.setArguments(['crawl', 'aliexpress'])
        self._process.start()

    def process_finished(self):
        msg = QMessageBox()
        msg.setWindowTitle("Procces finished")
        msg.setText("Procces finished")
        msg.exec_()

    def change_save_path(self):
        with open(self.global_path.replace('\\', '/') + '/aliexpress/spiders/aliexpress.py') as f:
            lines = f.read().splitlines()
        with open(self.global_path.replace('\\', '/') + '/aliexpress/spiders/aliexpress.py', 'w') as f:
            count = 0
            for line in lines:
                count += 1
                if count == 17:
                    string = self.feeds_path
                    f.write(re.sub(r'"[^]]*"', '"' +
                            string[2::]+'"', line) + "\n")
                else:
                    f.write(line + '\n')

    def run_scrapy(self):
        result = subprocess.run(
            ['scrapy', 'crawl', 'test'], stdout=subprocess.PIPE)
        self.text.setText(result.stdout.decode('utf-8'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ScrapyGUI()
    sys.exit(app.exec_())
