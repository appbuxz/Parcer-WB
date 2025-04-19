import asyncio
from playwright.async_api import async_playwright
from datetime import datetime

async def main():
    async with async_playwright() as p:
        # Запуск браузера Firefox
        browser = await p.firefox.launch()
        page = await browser.new_page()

        # Открываем URL
        url = "https://www.wildberries.ru/catalog/31299196/detail.aspx"  # Ссылка на нужный сайт
        await page.goto(url)

        # Ожидаем появления всех контейнеров с нужным классом
        await page.wait_for_selector('.price-block__price')

        # Получаем первый элемент с нужным классом (если нужен только один)
        container = await page.query_selector('.price-block__price')
        priceprod = None  # Инициализируем переменную

        if container:
            # Проверяем наличие <ins> внутри контейнера
            ins_element = await container.query_selector('ins')

            if ins_element:
                print("Найден элемент <ins> внутри контейнера.")

                # Ищем дочерние элементы <span>
                span_elements = await container.query_selector_all('span')

                # Извлекаем текст первого <span>, если он существует
                if span_elements:
                    span_text = await span_elements[0].inner_text()
                    priceprod = span_text.strip()  # Удаляем лишние пробелы
                    print(f"Цена товара: {priceprod}")
                else:
                    print("Элемент <span> не найден.")
            else:
                print("Элемент <ins> не найден внутри контейнера.")
        else:
            print("Контейнер с указанным классом не найден.")

        await browser.close()
        return priceprod

# Функция для записи данных в файл
def txtprint(formatted_time, pricetext):
    with open(r'C:\VS CODE\py\data.txt', 'a', encoding='utf-8') as f:  # Обратите внимание на 'r' перед строкой пути
        f.write(f"Дата и время: {formatted_time}, Цена товара: {pricetext}\n")

# Основная программа
if __name__ == "__main__":
    # Получаем текущую дату и время
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    # Запускаем асинхронную функцию
    price = asyncio.run(main())

    # Проверяем, что цена была найдена, и записываем её в файл
    if price:
        txtprint(formatted_time, price)
    else:
        print("Цена не найдена, запись в файл не выполнена.")
