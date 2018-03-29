import scrapy
from random import randint

class ThanhNienSpider(scrapy.Spider):
    name = "thanhnien"
    BASE_URL = 'http://thanhnien.vn' 

    def start_requests(self):
        url = self.BASE_URL
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        links = response.css('#mainmenu a::attr(href)') .extract()
        normal_links = [self.BASE_URL + x for x in links if not x.startswith('http') and "javascript" not in x]
        full_links = [x for x in links if x.startswith('http') and "media" not in x]
        for link in full_links:
            yield scrapy.Request(link, callback=self.parse_full_links)
        for link in normal_links:
            yield scrapy.Request(link, callback=self.parse_links)

    def parse_full_links(self, response):
        links = response.css('#submenu a::attr(href)').extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_links)

    def parse_links(self, response):
        links = response.css('article header a::attr(href)').extract()
        paging = response.css('#paging ul li:last-child a::attr(href)').extract_first()
        viewdate = response.css('a.viewdate-btn::attr(href)').extract_first()
        if viewdate is not None:
            yield scrapy.Request(url = self.BASE_URL + viewdate, callback = self.parse_links)
        else:
            links = list(map(lambda x : self.BASE_URL + x if not x.startswith('http') else x, links ))
            for link in links:
                yield scrapy.Request(link, callback = self.parse_content)
            if paging:
                yield scrapy.Request(url = self.BASE_URL + paging, callback = self.parse_links)

    def parse_content(self, response):
        title = response.css('.main-title::text').extract_first()
        summary = response.css('#chapeau').xpath('.//text()').extract()
        content = response.css('#abody').xpath('.//text()').extract()
        cat = response.css('.sub a::text').extract_first()
        date = response.css('.meta time::text').extract_first()
        content = '\n'.join(content).lstrip().rstrip()
        summary = '\n'.join(summary).lstrip().rstrip()
        yield {'_id': response.url, 'date': date, 'title': title, 'summary': summary, 'content': content, 'type': cat}

