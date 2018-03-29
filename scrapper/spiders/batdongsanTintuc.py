import scrapy
from random import randint

class BatdongsanTintucSpider(scrapy.Spider):
	name = "batdongsanTintuc"
	BASE_URL = 'http://www.batdongsan.vn'

	def start_requests(self):
		url = self.BASE_URL
		yield scrapy.Request(url=url, callback=self.parse)

	def parse(self,response):
		links = ['/tin-tuc/phong-thuy.html']
		print('******************Links*******************')
		print(links)
		for link in links:
			link = response.urljoin(link)
			print('***********link_update********************')
			print(link)
			yield scrapy.Request(link, callback=self.parse_links)
			print('*********yield_parse***********')

	def parse_links(self, response):
		subLinks = response.css('div.articel-news-items-list.row h3.news-items-title a::attr(href)').extract()
		print('****************subLinks*********************')
		print(subLinks)
		for subLink in subLinks:
			subLink = response.urljoin(subLink)
			print('**************sublink_update*******************')
			print(subLink)
			yield scrapy.Request(subLink, callback=self.parse_content)
			print('**********yield_parse_links**********')

		pagging = response.css('a.next.btn.btn-pagging::attr(href)').extract_first()
		print('*************pagging****************')
		print(pagging)
		if pagging:
			pagging = response.urljoin(pagging)
			print('************pagging_update*************')
			print(pagging)
			yield scrapy.Request(pagging, callback=self.parse_links)
			print('*********yield_parse_links*******')

	def parse_content(self, response):
		print("***********Content**********")
		title = response.css('h2.AL_Title1::text').extract_first().lstrip().rstrip()
		summary = response.css('div.A_Content *::text').extract_first().lstrip().rstrip()
		content = response.css('div.A_Content *::text').extract()
		content.pop(0)
		while len(content[-1]) < 35:
			content.pop()
		cat = 'phong thủy'
		date = response.css('span.PostDate span::text').extract_first()
		content = '\n'.join(content).lstrip().rstrip()
		yield {'_id': response.url, 'date': date, 'title': title, 'summary': summary, 'content': content, 'type': cat}
		print('********yield_parse_content*********')