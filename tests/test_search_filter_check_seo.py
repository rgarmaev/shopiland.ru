import time
import pytest
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver


@pytest.fixture(scope="module")
def web_browser():
    # Инициализация WebDriver (можно использовать Chrome)
    driver_path = 'C:/driver/chrome_driver/chromedriver.exe'
    browser = webdriver.Chrome()
    yield browser
    browser.quit()


def test_search_relevance(web_browser):
    # Открыть сайт
    web_browser.get("https://shopiland.ru/")
    time.sleep(5)
    # Ввести запрос в поиск
    search_input = web_browser.find_element(By.XPATH, "//input[@type='text']")
    search_input.send_keys("кошелек")
    time.sleep(5)
    # Нажать кнопку поиска
    search_button = web_browser.find_element(By.XPATH, "//button[@type='submit']")
    search_button.click()
    time.sleep(5)
    # Проверить результаты поиска
    search_results = WebDriverWait(web_browser, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//p[@class='css-99ww93']"))
    )
    #assert len(search_results) > 0, "No search results found"

    # Проверка релевантности результатов
    for result in search_results:
        title_element = result.find_element(By.XPATH, "//p[@class='css-99ww93']")
        product_title = title_element.text.lower()
        assert "кошелек" in product_title, f"Search result not relevant: {product_title}"
    # Проверяем, что все магазины отображают результаты
    marketplaces = web_browser.find_elements(By.XPATH, "//span[@class='css-tcshld']/following-sibling::span[@class='css-18woau7']")
    print(marketplaces)
    for marketplace in marketplaces:
        # Проверяем, что есть результаты поиска для каждого магазина
        search_results = web_browser.find_elements(By.XPATH, f"//span[@class='css-18woau7']")
        assert search_results > 0, f"No search results found for {marketplace}"

        # Проверяем, что товары присутствуют на сайте магазина
        for result in search_results:
            marketplace_link = result.find_element(By.XPATH, "./a").get_attribute('href')
            web_browser.get(marketplace_link)
            time.sleep(2)  # Добавляем задержку для полной загрузки страницы
            assert len(web_browser.find_elements(By.XPATH, "//div[@class='product-item']")) > 0, f"No products found on {marketplace} website"


def test_sort_by_popularity(web_browser):
    # Открыть сайт
    web_browser.get("https://shopiland.ru/")

    # Ввести запрос в поиск
    search_input = web_browser.find_element(By.XPATH, "//input[@type='text']")
    search_input.send_keys("кошелек")  # Пример запроса для теста

    # Нажать кнопку поиска
    search_button = web_browser.find_element(By.XPATH, "//button[@type='submit']")
    search_button.click()
    time.sleep(5)
    # Нажать на сортировку по популярности
    popularity_sort_button = web_browser.find_element(By.XPATH, '//button[@type="button" and @value="popular"]')
    popularity_sort_button.click()  # Пример выбора сортировки по рейтингу

    # Проверить, что первый товар имеет больше всего отзывов (считаем по кол-ву отзывов)
    product_reviews = web_browser.find_elements(By.XPATH,"//span[@class='css-1t0tstb']")
    reviews_counts = [int(review.text.split()[0]) for review in product_reviews]

    # Получить количество отзывов для первого товара
    first_product_reviews = reviews_counts[0]

    # Проверить, что количество отзывов для первого товара больше, чем у всех остальных
    assert first_product_reviews > max(reviews_counts[1:]), "First product does not have the most reviews"


def test_seo_check(web_browser):
    # Открыть сайт
    web_browser.get("https://shopiland.ru/")

    # Проверить наличие canonical link на странице
    canonical_link = web_browser.find_element(By.XPATH, "//link[@rel='canonical']")
    assert canonical_link, "Canonical link not found"

    # Проверить скорость ответа от маркетплейсов
    response_time = web_browser.execute_script(
        "return performance.timing.responseStart - performance.timing.navigationStart;")
    assert response_time < 20000, "Response time exceeds 20 seconds"

    # Проверить alt атрибуты для всех изображений
    images = web_browser.find_elements(By.XPATH, "//img")
    for image in images:
        alt_attribute = image.get_attribute("alt")
        assert alt_attribute, "Alt attribute missing for image"