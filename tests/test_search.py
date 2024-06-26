import time
import logging
import pytest
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pages.locators
from pages.base import HomePage, SearchResultsPage, SearchResultsMarketplaces
from pages.locators import HomePageLocators, ProductPageLocators, SearchResultsLocatorMarketplaces
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
marketplaces_with_products_not_found = []
def read_search_text():
    with open("text_search.txt", "r", encoding="utf-8") as file:
        search_text = file.read().strip()
    return search_text

@pytest.fixture(scope="module")
def web_browser():
    driver_path = 'C:/driver/chrome_driver/chromedriver.exe'
    browser = webdriver.Chrome()
    yield browser
    browser.quit()

def test_search_relevance(web_browser):
    home_page = HomePage(web_browser)
    home_page.open('https://shopiland.ru/')
    search_text = read_search_text()
    time.sleep(5)
    home_page.search_product(search_text, HomePageLocators.SEARCH_INPUT, HomePageLocators.SEARCH_BUTTON)
    time.sleep(5)
    results_page = SearchResultsPage(web_browser)
    search_results = results_page.get_product_titles()

    for result in search_results:
        product_title = result.text.lower()
        assert search_text.lower() in product_title, f"Результат поиска не соответствует запросу: {product_title}"
    print(f"Результат поиска соответствует запросу: {search_text} = {product_title}")

def test_search_marketplace(web_browser):
    home_page = HomePage(web_browser)
    home_page.open('https://shopiland.ru/')
    search_text = read_search_text()
    home_page.search_product(search_text, HomePageLocators.SEARCH_INPUT, HomePageLocators.SEARCH_BUTTON)
    time.sleep(5)
    results_page = SearchResultsMarketplaces(web_browser)

    # Список имен маркетплейсов
    marketplace_names = ['oz', 'al', 'wb', 'ym', 'sm', 'ke']

    marketplaces_with_products = []

    time.sleep(20)
    for marketplace_name in marketplace_names:
        # Получаем список товаров для текущего маркетплейса
        marketplace_products = getattr(results_page, f'get_marketplace_{marketplace_name}')()

        # Проверяем, что marketplace_products является списком
        if isinstance(marketplace_products, list):
            products_found = False

            # Перебираем каждый элемент списка товаров для данного маркетплейса
            for product_element in marketplace_products:
                # Получаем текст элемента и разделяем его по пробелам
                product_text_parts = product_element.text.split()

                if len(product_text_parts) > 1:
                    number_of_products_text = product_text_parts[1]  # количество товаров

                    # Пробуем преобразовать текст в целое число
                    try:
                        number_of_products = int(number_of_products_text)
                        if number_of_products > 0:
                            products_found = True
                            break  # Если найден хотя бы один товар, прекращаем поиск
                    except ValueError:
                        pass  # Пропускаем элемент, если не удалось преобразовать текст в число

            if products_found:
                print(f"На маркетплейсе {marketplace_name} найдено товаров: {number_of_products}")
                marketplaces_with_products.append(marketplace_name)
            else:
                print(f"На маркетплейсе {marketplace_name} не найдено ни одного товара")
                marketplaces_with_products_not_found.append(marketplace_name)
        else:
            print(f"На маркетплейсе {marketplace_name} не найдено ни одного товара")
            marketplaces_with_products_not_found.append(marketplace_name)
    assert marketplaces_with_products, "На ни одном маркетплейсе не найдено ни одного товара"
    print("Товары найдены на следующих маркетплейсах:", marketplaces_with_products)





def test_marketplace_search_results(web_browser):
    # Функция для выполнения поиска на странице маркетплейса
    home_page = HomePage(web_browser)
    home_page_url = 'https://megamarket.ru/'
    home_page.open(home_page_url)
    time.sleep(10)
    # Ожидание кнопки закрытия баннера на странице маркетплейса
    #web_browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    marketplace_close_button = WebDriverWait(web_browser, 10).until(
        EC.element_to_be_clickable(pages.locators.HomePageLocators.MARKETPLACE_CLOSE_SM)
    )
    marketplace_close_button.click()
    logging.info("Попытка нажать кнопку поиска")
    # Выполняем поиск на странице маркетплейса
    search_text = read_search_text()
    time.sleep(5)
    # Ожидание окна ввода на странице маркетплейса
    marketplace_search_input = WebDriverWait(web_browser, 10).until(
        EC.element_to_be_clickable(SearchResultsLocatorMarketplaces.SEARCH_INPUT_SM)
    )
    marketplace_search_input.clear()
    marketplace_search_input.send_keys(search_text)
    marketplace_search_input.send_keys(Keys.ENTER)
    time.sleep(10)
    results_page = SearchResultsMarketplaces(web_browser)
    search_results = results_page.get_product_titles_sm()

    for result in search_results:
        product_title = result.text.lower()
        assert search_text.lower() in product_title, f"Результат поиска не соответствует запросу: {product_title}"
    print(f"Результат поиска соответствует запросу: {search_text} = {product_title}")

def test_sort_by_popularity(web_browser):
    home_page = HomePage(web_browser)
    home_page.open('https://shopiland.ru/')
    search_text = read_search_text()
    time.sleep(5)
    home_page.search_product(search_text, HomePageLocators.SEARCH_INPUT, HomePageLocators.SEARCH_BUTTON)
    results_page = SearchResultsPage(web_browser)

    popularity_sort_button = WebDriverWait(web_browser, 10).until(
        EC.element_to_be_clickable(ProductPageLocators.POPULARITY_SORT_BUTTON)
    )
    popularity_sort_button.click()

    product_reviews = results_page.get_product_reviews()
    reviews_counts = [int(review.text.split()[0]) for review in product_reviews]

    first_product_reviews = reviews_counts[0]
    assert first_product_reviews >= max(reviews_counts[1:]), "Первый товар не имеет наибольшее количество отзывов"

def test_sort_by_rating(web_browser):
    home_page = HomePage(web_browser)
    home_page.open('https://shopiland.ru/')
    search_text = read_search_text()
    time.sleep(5)
    home_page.search_product(search_text, HomePageLocators.SEARCH_INPUT, HomePageLocators.SEARCH_BUTTON)
    results_page = SearchResultsPage(web_browser)

    rating_sort_button = WebDriverWait(web_browser, 10).until(
        EC.element_to_be_clickable(ProductPageLocators.RATING_SORT_BUTTON)
    )
    rating_sort_button.click()

    # Получаем список отзывов о продуктах
    product_reviews = results_page.get_product_reviews()

    # Создаем пустой список для сохранения количества отзывов
    reviews_counts = []

    # Итерируемся по каждому элементу списка отзывов
    for review in product_reviews:
        # Пытаемся получить текст элемента отзыва
        try:
            review_text = review.text
        except StaleElementReferenceException:
            # Если элемент стал устаревшим, пропускаем его
            continue

        # Разбиваем текст отзыва и получаем количество отзывов
        review_count = int(review_text.split()[0])
        reviews_counts.append(review_count)

    # Проверяем, что первый товар имеет наибольший рейтинг
    first_product_reviews = reviews_counts[0]
    assert first_product_reviews >= max(reviews_counts[1:]), "Первый товар не имеет наибольший рейтинг"
def test_seo_check(web_browser):
    home_page = HomePage(web_browser)
    home_page.open('https://shopiland.ru/')
    time.sleep(5)

    canonical_link = WebDriverWait(web_browser, 10).until(
        EC.presence_of_element_located(HomePageLocators.CANONICAL_LINK)
    )
    assert canonical_link, "Каноническая ссылка не найдена"

    all_images = home_page.get_elements(HomePageLocators.ALL_IMAGES)
    for image in all_images:
        alt_attribute = image.get_attribute("alt")
        assert alt_attribute, "Отсутствует атрибут alt у изображения"


#Результаты поиска должны быть релевантны запросу;+
#товары должны быть во всех магазинах.+
#Если в каком-то маркетплейсе не оказалось товаров,
#то следует проверить его выдачу прямым запросом на сайт маркетплейса.

#Проверьте отображение товаров для выбранного города.
#Для этого запросите результаты в определенном магазине.
#Товары сравниваются, так как парсеры параллельно выполняют запрос
#пользователя во всех магазинах с выбранным городом.

#Если в поиске выбран, например, город Омск, то при переходе на страницу товара
#в магазине товар должен быть доступен для продажи в выбранном городе.

