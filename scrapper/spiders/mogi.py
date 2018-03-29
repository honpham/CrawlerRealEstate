import scrapy
from random import randint

class BatdongsanTintucSpider(scrapy.Spider):
	name = "mogi"
	BASE_URL = 'https://mogi.vn/'
	count = 1
	def start_requests(self):
		url = self.BASE_URL
		yield scrapy.Request(url=url, callback=self.parse)

	def parse(self,response):
		links = ['/thue-nha-dat?cp=1']
		print('******************Links*******************')
		print(links)
		for link in links:
			link = response.urljoin(link)
			print('***********link_update********************')
			print(link)
			yield scrapy.Request(link, callback=self.parse_links)
			print('*********yield_parse***********')

	def parse_links(self, response):
		subLinks = response.css('.title2 a::attr(href)').extract()
		print('****************subLinks*********************')
		print(subLinks)
		for subLink in subLinks:
			subLink = response.urljoin(subLink)
			print('**************sublink_update*******************')
			print(subLink)
			yield scrapy.Request(subLink, callback=self.parse_content)
			print('**********yield_parse_links**********')

		#pagging = response.css('.pagination li:last-child a::attr(href)').extract_first()
		#print('*************pagging****************')
		#print(pagging)
		if self.count < 101:
			self.count = self.count + 1
			pagging = '/thue-nha-dat?cp=' + str(self.count)
			page = response.urljoin(pagging)
			print('************pagging_update*************')
			print(page)
			yield scrapy.Request(page, callback=self.parse_links)
			print('*********yield_parse_links*******')

	def parse_content(self, response):
		print("***********Content**********")
		title = response.css('.title::text').extract_first().lstrip().rstrip()
		content = response.css('.property-info-content::text').extract()
		content = '\n'.join(content).lstrip().rstrip()
		cat = 'Tìm thuê'
		address = response.css('.address::text').extract_first().lstrip().rstrip()
		area = response.css('.property-info li:nth-child(2)::text').extract_first().lstrip().rstrip()
		area = area[1:].lstrip()
		if area == '':
			area = response.css('.property-info li:nth-child(3)::text').extract_first().lstrip().rstrip()
			area = area[1:].lstrip()
		price = response.css('.property-info li:nth-child(1)::text').extract_first().lstrip().rstrip()
		price = price[1:].lstrip()
		interior = ''
		realestate = ''
		yield {'_id': response.url, 'title': title, 'content': content, 'address': address, 'area': area, 'price': price, 'transactionType': cat, 'interior': interior, 'realStateType': realestate}
		print('********yield_parse_content*********')