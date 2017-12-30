import lxml.html
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import scraper as sc


class Scraping:

    def __init__(self):
        self.url = 'https://www.fulgentgenetics.com/products/carrierscreening/calculator.html'
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        self.data = []
        # self.buttons = self.driver.find_elements_by_xpath('//select[@id="combobox"]/option[not(@style)]')
        self.default_button = self.driver.find_element_by_xpath('//button[@data-id="combobox"]')
        # self.options = self.driver.find_element_by_xpath('//ul[@aria-expanded="false"]')

    def get_data(self):
        for index in range(2, 386):
            self.default_button.click()
            self.options = self.driver.find_elements_by_xpath('//ul[@aria-expanded="true"]/li')
            self.options[index].click()
            self.tree = lxml.html.fromstring(self.driver.page_source)
            self.condition = self.tree.xpath('//button[@data-id="combobox"]/span/text()')[0]
            self.results = [self.condition]
            print(self.condition)
            self.check_risk = self.driver.find_element_by_xpath('//div[@id="SubmitButtonWrapper"]')
            self.check_if_condition_xlinked()
            self.data.append(self.results)
        sc.Database(('Condition', 'M+F+', 'M+F-', 'M+F?', 'M-F+', 'M-F-', 'M-F?', 'M?-F+', 'M?-F-', 'M?F?')).push_data(self.data)

    def check_if_condition_xlinked(self):
        if not 'X-linked' in self.condition:
            self.mother_options = self.driver.find_elements_by_xpath(
                '//div[@id="motherWrapper"]//div[@class="RadioWrapper"]//input')
            self.father_options = self.driver.find_elements_by_xpath(
                '//div[@id="fatherWrapper"]//div[@class="RadioWrapper"]//input')
            self.check_options_normal()
        else:
            self.mother_options = self.driver.find_elements_by_xpath(
                '//div[@id="motherWrapper"]//div[@class="RadioWrapper"]//input')
            self.check_options_xlinked()

    def check_options_normal(self):
        for element in self.mother_options:
            element.click()
            for second_element in self.father_options:
                second_element.click()
                self.check_risk.click()
                self.tree = lxml.html.fromstring(self.driver.page_source)
                self.results.append(self.tree.xpath('//div[@id="RiskPercentage"]/text()')[0])

    def check_options_xlinked(self):
        for element in self.mother_options:
            element.click()
            self.check_risk.click()
            self.results.append(self.tree.xpath('//div[@id="RiskPercentage"]/text()')[0])
            self.results.append('X-LINKED')
            self.results.append('X-LINKED')


Scraping = Scraping()
Scraping.get_data()