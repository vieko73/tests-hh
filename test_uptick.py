import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selene.api import *
from selene import browser
from selene.support.conditions import be


config.base_url = 'https://spb.hh.ru/'

def wait_for_page_load(main_component):
    browser.wait_for(browser.element(by.xpath(main_component)), be.visible, 15)

class TestClass(object):
    @classmethod
    def setup_class(cls):
        browser.set_driver(webdriver.Firefox(executable_path='./geckodriver'))

    @classmethod
    def teardown_class(cls):
        browser.close()

    def test_company_search(self):
        try:
            browser.open_url('')
            browser.element("select[data-qa='navi-search__select']").find(by.text('Компании')).click()
            input_field = browser.element("form[data-hh-tab-id='employersList'] input[placeholder='Я ищу…']")
            input_field.set_value("аптик")
            search_button = browser.element("form[data-hh-tab-id='employersList'] button[type='submit']")
            search_button.click()
            wait_for_page_load("//div[contains(text(), 'компаний найдено')]")
            uptick_element = browser.element(by.link_text("ООО «Аптик СПб»"))
            assert uptick_element.should(be.visible)
        except NoSuchElementException as e:
            print("Element was not found. Exception was caught: %s" % e)
            raise e

    def test_vacancies_number(self):
        try:
            browser.open_url('employer/1886264')
            wait_for_page_load("//h3[text()='Вакансии компании']")
            vacancies_number = browser.element(by.xpath("//span[contains(text(), 'Вакансии в текущем регионе')]/following-sibling::span")).text
            assert int(vacancies_number) == 8
            #number of vacancies is changed from 9 to 8 due to changes on the site
        except NoSuchElementException as e:
            print("Element was not found. Exception was caught: %s" % e)
            raise e

    def test_qa_vacancy(self):
        try:
            browser.open_url('employer/1886264')
            wait_for_page_load("//h3[text()='Вакансии компании']")
            qa_vacancy = browser.element(by.xpath("//span[contains(text(), 'Вакансии в текущем регионе')]/ancestor::h4/following-sibling::div//a[text()='QA Automation Engineer']"))
            assert qa_vacancy.should(be.visible)
        except NoSuchElementException as e:
            print("Element was not found. Exception was caught: %s" % e)
            raise e

