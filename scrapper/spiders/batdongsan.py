import scrapy
from random import randint

class BatdongsanSpider(scrapy.Spider):
    name = "batdongsan"
    BASE_URL = 'http://www.batdongsan.vn'

    def start_requests(self):
        url = self.BASE_URL
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self,response):
        links = ['/giao-dich/cho-thue-nha-dat.html']
        print('******************Links*******************')
        print(links)
        for link in links:
            link = response.urljoin(link)
            print('***********link_update********************')
            print(link)
            yield scrapy.Request(link, callback=self.parse_links)
            print('*********yield_parse***********')

    def parse_links(self, response):
        subLinks = response.css('#cat_0 h2.P_Title a::attr(href)').extract()
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
        position = response.css('.details-warp-item label::text').extract()
        paddress = position.index('Địa chỉ:') + 1
        if paddress == 5:
            address = response.css('.details-warp-item:nth-child(5) span::text').extract_first().lstrip().rstrip()
            area = response.css('.details-warp-item:nth-child(7) span::text').extract_first().lstrip().rstrip()
            price = response.css('.details-warp-item:nth-child(6) span::text').extract_first().lstrip().rstrip()
        elif paddress == 4:
            address = response.css('.details-warp-item:nth-child(4) span::text').extract_first().lstrip().rstrip()
            area = response.css('.details-warp-item:nth-child(6) span::text').extract_first().lstrip().rstrip()
            price = response.css('.details-warp-item:nth-child(5) span::text').extract_first().lstrip().rstrip()
        else:
            address = response.css('.details-warp-item:nth-child(6) span::text').extract_first().lstrip().rstrip()
            area = response.css('.details-warp-item:nth-child(8) span::text').extract_first().lstrip().rstrip()
            price = response.css('.details-warp-item:nth-child(7) span::text').extract_first().lstrip().rstrip()
        title = response.css('div.P_Title1.hidden-xs h1::text').extract_first().lstrip().rstrip()
        content = response.css('div.PD_Gioithieu::text').extract()
        content = '\n'.join(content).lstrip().rstrip()
        cat = 'Cho thuê'
        interior = ''
        realestate = response.css('.details-warp-item:nth-child(2) span::text').extract_first().lstrip().rstrip()
        yield {'_id': response.url, 'title': title, 'content': content, 'address': address, 'area': area, 'price': price, 'transactionType': cat, 'interior': interior, 'realStateType': realestate}
        print('********yield_parse_content*********')