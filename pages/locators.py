from selenium.webdriver.common.by import By

class HomePageLocators:
    SEARCH_INPUT = (By.XPATH, "//input[@type='text']")
    SEARCH_BUTTON = (By.XPATH, "//button[@type='submit']")
    CANONICAL_LINK = (By.XPATH, "//link[@rel='canonical']")
    ALL_IMAGES = (By.XPATH, "//img")
    MARKETPLACE_CLOSE_SM = (By.XPATH, "//button[@type='button' and @class='close-button mass-communication__close']") #//*[name()='svg'][@class='svg-icon']
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
    MARKETPLACE_SEARCH_BUTTON_YM = (By.XPATH, "//input[@type='text']")
    MARKETPLACE_SEARCH_BUTTON_SM = (By.XPATH, "//button[@aria-label='Искать']")
    SEARCH_INPUT_SM = (By.XPATH, "//input[@type='search' and contains(@placeholder, 'Искать')]") #button.sumbit //input[@type='search']
    SEARCH_INPUT_YM = (By.XPATH, "//input[@type='text']")
    MARKETPLACE_PRODUCT_TITLES_YM = (By.XPATH, "//p[@role='link']")
    MARKETPLACE_PRODUCT_TITLES_SM = (By.XPATH, "//a[@class='ddl_product_link']")

class ProductPageLocators:
    PRODUCT_TITLES = (By.XPATH, "//p[@class='css-99ww93']")
    PRODUCT_REVIEWS = (By.XPATH, "//span[@class='css-1t0tstb']")
    POPULARITY_SORT_BUTTON = (By.XPATH, '//div[contains(@class, "MuiBox-root") and contains(text(), "популярности")]')
    RATING_SORT_BUTTON = (By.XPATH, '//div[contains(@class, "MuiBox-root") and contains(text(), "рейтингу")]')

