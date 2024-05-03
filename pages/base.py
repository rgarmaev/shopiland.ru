from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.locators import ProductPageLocators, SearchResultsPageLocators, HomePageLocators, SearchResultsLocatorMarketplaces

class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.locators = HomePageLocators


    def open(self, url):
        self.driver.get(url)

    def search_product(self, product_name, search_input_locator, search_button):
        search_input = self.driver.find_element(*search_input_locator)
        search_input.clear()
        search_input.send_keys(product_name)
        search_button = self.driver.find_element(*search_button)
        search_button.click()

    def click_close_button(self, by_locator):
        return self.driver.find_element(*by_locator)

    def get_element(self, by_locator):
        return self.driver.find_element(*by_locator)

    def get_elements(self, by_locator):
        return self.driver.find_elements(*by_locator)


class SearchResultsPage:
    def __init__(self, driver):
        self.driver = driver
        self.locators = SearchResultsPageLocators

    def get_product_titles(self):
        return self.driver.find_elements(*self.locators.PRODUCT_TITLES)

    def get_product_reviews(self):
        return self.driver.find_elements(*ProductPageLocators.PRODUCT_REVIEWS)


class SearchResultsMarketplaces:
    def __init__(self, driver):
        self.driver = driver
        self.locators = SearchResultsLocatorMarketplaces
        self.marketplace_methods = {
            'oz': self.get_marketplace_oz,
            'al': self.get_marketplace_al,
            'wb': self.get_marketplace_wb,
            'ym': self.get_marketplace_ym,
            'sm': self.get_marketplace_sm,
            'ke': self.get_marketplace_ke
        }

    def get_marketplace_oz(self):
        return self.driver.find_elements(*self.locators.MARKETPLACE_LINKS_OZ)

    def get_marketplace_al(self):
        return self.driver.find_elements(*self.locators.MARKETPLACE_LINKS_AL)

    def get_marketplace_wb(self):
        return self.driver.find_elements(*self.locators.MARKETPLACE_LINKS_WB)

    def get_marketplace_ym(self):
        return self.driver.find_elements(*self.locators.MARKETPLACE_LINKS_YM)

    def get_marketplace_sm(self):
        return self.driver.find_elements(*self.locators.MARKETPLACE_LINKS_SM)

    def get_marketplace_ke(self):
        return self.driver.find_elements(*self.locators.MARKETPLACE_LINKS_KE)

    def search_marketplace_ym(self):
        return self.driver.find_element(*self.locators.MARKETPLACE_SEARCH_BUTTON_YM)

    def search_marketplace_sm(self):
        return self.driver.find_element(*self.locators.MARKETPLACE_SEARCH_BUTTON_SM)

    def get_product_titles_sm(self):
        return self.driver.find_elements(*self.locators.MARKETPLACE_PRODUCT_TITLES_SM)

    def get_product_titles_ym(self):
        return self.driver.find_elements(*self.locators.MARKETPLACE_PRODUCT_TITLES_YM)

class ProductPage:
    def __init__(self, driver):
        self.driver = driver
        self.locators = ProductPageLocators

    def open(self, url):
        self.driver.get(url)

    def get_product_reviews(self):
        return self.driver.find_elements(*self.locators.PRODUCT_REVIEWS)
