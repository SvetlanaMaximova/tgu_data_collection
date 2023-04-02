"""Соберите информацию о заквасках с сайта pro-syr.ru
(https://pro-syr.ru/zakvaski-dlya-syra/mezofilnye/)
Необходимо собрать следующие данные:
•	Название продукта
•	Цена
•	Есть ли продукт в наличии
Результат должен быть записан в CSV файл
"""

import scrapy
import time


class BootguSpider(scrapy.Spider):
    name = "bootgu"
    allowed_domains = ["pro-syr.ru"]
    start_urls = ["https://pro-syr.ru/zakvaski-dlya-syra/mezofilnye/"]

    def parse(self, response):
        links = response.css("div.nameproduct a::attr(href)")
        for link in links:
            time.sleep(3)
            yield response.follow(link, self.parse_product)

        link = response.css("ul.pagination a::attr(href)")[-1].get()
        yield response.follow(link, self.parse)

    def parse_product(self, response):
        price = response.css("span.autocalc-product-price::text").get()
        price = price.replace('руб.', '')
        price = price.replace(' ', '')
        yield {
            "name": response.css("div.col-md-9 h1::text").get(),
            "price": price,
            "availability": response.css("div.product-description b::text").get()
        }





