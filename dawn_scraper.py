import scrapy
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('localhost', 27017, connect=False)
db_articles = client['articles']
collection = db_articles['article']

class NewsArchiveScrapper(scrapy.Spider):
	name = "news_archive"
	start_urls = ['https://www.dawn.com']

	def parse(self, response):
		link = "https://www.dawn.com/newspaper/{0}/{1}-{2}-{3}"
		categories = ['front-page', 'back-page', 'national', 'business', 'international', 'sport']
		for category in categories:
			for year in range(2001, 2021):
				for month in range(1, 13):
					if month < 10:
						month = "0"+str(month)
					for day in range(1, 32):
						if day < 10:
							day = "0"+str(day)
						parsed_link = link.format(category, year, month, day)
						request = scrapy.Request(parsed_link, callback=self.parse_page, meta={
								'category': category,
								'date': "{}-{}-{}".format(month, day, year)
							})
						yield request

	
	def parse_page(self, response):
		data = []
		SET_SELECTOR = '.story--large'
		for res in response.css(SET_SELECTOR):
			data.append(res.css('.story__title a ::attr(href)').extract_first())
		SET_SELECTOR = '.story--small'
		for res in response.css(SET_SELECTOR):
			data.append(res.css('.story__title a ::attr(href)').extract_first())

		print("<><><><><>LENGTH: ", len(data))

		for link in data:
			print(">>>>>>LINK: ", link)
			request = scrapy.Request(
					url=link,
					callback=self.parse_article,
					meta={
						'category': response.meta.get('category'),
						'date': response.meta.get('date')
					}
				)
			yield request
			
		print("I came template__header")

	def parse_article(self, response):
		print('>>>>>>RES: ', response)
		SET_SELECTOR = '.template__header'
		# articles = []
		header = response.css(SET_SELECTOR)[0]

		# date_string = response.meta.get('date')
		# date_format = "%m-%d-%Y"
		# date = int(datetime.strptime(date_string, date_format).timestamp())
		
		title = header.css('.story__title ::text').extract_first()
		image_src = header.css('.media__item picture img::attr(src)').extract_first()

		print("---------")
		print("Image: ", image_src)
		print("----------")

		# article = {
		# 	'title': title.replace("\n", ""),
		# 	'date': date,
		# 	'category': response.meta.get('category'),
		# 	'indexed': False,
		# 	'image_src': image_src
		# }
		# content = response.css('.template__main')
		# article['content'] = ' '.join(content.css('.story__content p ::text').extract())
		collection.update_one({'title': title}, {'$set': {'image_src': image_src}})
		