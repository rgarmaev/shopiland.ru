from selenium.webdriver.common.by import By

class HomePageLocators:
    SEARCH_INPUT = (By.XPATH, "//input[@type='text']")
    SEARCH_BUTTON = (By.XPATH, "//button[@type='submit']")
    CANONICAL_LINK = (By.XPATH, "//link[@rel='canonical']")
    ALL_IMAGES = (By.XPATH, "//img")

class SearchResultsPageLocators:
    PRODUCT_TITLES = (By.XPATH, "//p[@class='css-99ww93']")

class SearchResultsLocatorMarketplaces:
    MARKETPLACE_LINKS_OZ = (By.XPATH, "//span[contains(text(), 'Ozon') and contains (@calss, css-18woau7)]")
    MARKETPLACE_LINKS_AL = (By.XPATH, "//span[contains(text(), 'AliExpress') and contains (@calss, css-18woau7)]")
    MARKETPLACE_LINKS_WB = (By.XPATH, "//span[contains(text(), 'Wildberries') and contains (@calss, css-18woau7)]")
    MARKETPLACE_LINKS_YM = (By.XPATH, "//span[contains(text(), 'Яндекс Маркет') and contains (@calss, css-18woau7)]")
    MARKETPLACE_LINKS_SM = (By.XPATH, "//span[contains(text(), 'СберМегамаркет') and contains (@calss, css-18woau7)]")
    MARKETPLACE_LINKS_KE = (By.XPATH, "//span[contains(text(), 'KazanExpress') and contains (@calss, css-18woau7)]")
    PRODUCT_TITLES = (By.XPATH, "//p[@class='css-99ww93']")

class ProductPageLocators:
    PRODUCT_TITLES = (By.XPATH, "//p[@class='css-99ww93']")
    PRODUCT_REVIEWS = (By.XPATH, "//span[@class='css-1t0tstb']")
    POPULARITY_SORT_BUTTON = (By.XPATH, '//div[contains(@class, "MuiBox-root") and contains(text(), "популярности")]')

