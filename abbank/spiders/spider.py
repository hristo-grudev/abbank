import scrapy

from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from ..items import AbbankItem
from itemloaders.processors import TakeFirst


class AbbankSpider(scrapy.Spider):
	name = 'abbank'
	start_urls = ['https://www.abbank.com/about-abb/in-the-news']

	def parse(self, response):
		post_links = response.xpath('//div[@class="content"]//child::node()').getall()
		description = []
		title = ''
		for el in post_links:
			tag = el[1:3]
			if 'h2' in tag:
				description = [p.strip() for p in description]
				description = ' '.join(description).strip()
				if len(description) > 2:
					item = ItemLoader(item=AbbankItem(), response=response)
					item.default_output_processor = TakeFirst()
					item.add_value('title', title)
					item.add_value('description', description)
					yield item.load_item()
				title = remove_tags(el)
				description = []
			else:
				description.append(remove_tags(el))

		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		item = ItemLoader(item=AbbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		yield item.load_item()
