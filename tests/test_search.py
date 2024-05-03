import time
import logging
import pytest
from selenium import webdriver
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
    home_page_url = 'https://shopiland.ru/'
    def search_on_marketplace(home_page_url, search_text, marketplace_name, button_locator, product_titles_locator,
                              search_input_locator):
        home_page = HomePage(web_browser)
        home_page.open(home_page_url)
        time.sleep(10)

        # Нажимаем кнопку закрытия если это маркетплейс "Megamarket" ('sm')
        if marketplace_name == 'sm':
            marketplace_close_button = WebDriverWait(web_browser, 30).until(
                EC.element_to_be_clickable(pages.locators.HomePageLocators.MARKETPLACE_CLOSE_SM)
            )
            marketplace_close_button.click()
            home_page.click_close_button(pages.locators.HomePageLocators.MARKETPLACE_CLOSE_SM)

            # Пример логирования перед попыткой нажать кнопку поиска
            logging.info("Попытка нажать кнопку поиска")

            # Ожидание появления кнопки поиска на странице
            search_button = WebDriverWait(web_browser, 10).until(
                EC.element_to_be_clickable(button_locator)
            )

            # Нажатие на кнопку поиска
            search_button.click()

        # Выполняем поиск на странице маркетплейса
        home_page.search_product(search_text, search_input_locator, button_locator)

        # Добавляем небольшую задержку перед поиском элементов
        time.sleep(5)

        results_page = SearchResultsMarketplaces(web_browser)
        # Динамически вызываем метод get_product_titles_ {marketplace_name}
        return getattr(results_page, f'get_product_titles_{marketplace_name}')()

    # Данные для поиска и соответствующие URL маркетплейсов
    search_text = read_search_text()  # Функция для загрузки текста запроса из файла или переменной
    marketplace_data = {
        'sm': {'url': 'https://megamarket.ru',
               'button': pages.locators.SearchResultsLocatorMarketplaces.MARKETPLACE_SEARCH_BUTTON_SM,
               'product_titles': pages.locators.SearchResultsLocatorMarketplaces.MARKETPLACE_PRODUCT_TITLES_SM,
               'search_input': pages.locators.SearchResultsLocatorMarketplaces.SEARCH_INPUT_SM}
    }

    ym_search_successful = False  # Флаг успешного поиска на маркетплейсе Yandex Market

    for marketplace_name, data in marketplace_data.items():
        # Проверяем, на каком маркетплейсе не найдены товары
        if marketplace_name not in marketplaces_with_products_not_found:
            continue  # Пропускаем маркетплейсы, где товары уже были найдены
        time.sleep(15)
        # Выполняем поиск на маркетплейсе
        search_results = search_on_marketplace(data['url'], search_text, marketplace_name,
                                               data['button'], data['product_titles'], data['search_input'])

        if not search_results:
            print(f"На маркетплейсе {marketplace_name} не найдено ни одного товара")
            if marketplace_name == 'ym':
                ym_search_successful = False
            continue  # Переходим к следующему маркетплейсу

        # Проверяем результаты поиска
        for result in search_results:
            product_title = result.text
            assert search_text.lower() in product_title.lower(), f"Товар '{product_title}' на маркетплейсе {marketplace_name} не соответствует запросу '{search_text}'"

        print(f"Товары найдены на маркетплейсе {marketplace_name}")
        if marketplace_name == 'ym':
            ym_search_successful = True

    # Если на маркетплейсе Yandex Market не удалось найти товары, не пропускаем маркетплейс "sm"
    if not ym_search_successful:
        print("Поиск на маркетплейсе Yandex Market неуспешен. Продолжаем поиск на других маркетплейсах.")
        marketplaces_with_products_not_found.clear()  # Очищаем список маркетплейсов без товаров


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

    product_reviews = results_page.get_product_reviews()
    reviews_counts = [int(review.text.split()[0]) for review in product_reviews]

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

