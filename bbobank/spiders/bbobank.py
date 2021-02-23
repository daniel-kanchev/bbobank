import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from bbobank.items import Article


class BbobankSpider(scrapy.Spider):
    name = 'bbobank'
    start_urls = ['https://bbobank.ch/de/Infos/Aktuell']

    def parse(self, response):
        articles = response.xpath('//div[@class="content-col-bgcolor"][descendant::div[@class="wrap-news-title"]]')
        for article in articles:
            item = ItemLoader(Article())
            item.default_output_processor = TakeFirst()

            title = article.xpath('.//h2//text()').get()
            content = article.xpath('.//div[@class="wrap-news-text"]//text()').getall()
            content = [text for text in content if text.strip()]
            content = "\n".join(content).strip()

            item.add_value('title', title)
            item.add_value('content', content)

            yield item.load_item()
