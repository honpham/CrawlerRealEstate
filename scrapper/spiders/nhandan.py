import scrapy
from random import randint

class VnExpressSpider(scrapy.Spider):
    name = "nhandan"
    BASE_URL = 'http://www.nhandan.com.vn' 

    def start_requests(self):
        url = self.BASE_URL
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        links = response.css('#myNavbar > ul > li a::attr(href)').extract()
        for link in links:
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parse_links)
        
    def parse_links(self, response):
        links = response.css('div.media-body h3 a::attr(href)').extract()
        for link in links:
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parse_content)
        paging = response.css('ul.pagination li.next a::attr(href)').extract_first()
        if paging:
            paging = response.urljoin(paging)
            yield scrapy.Request(paging, callback=self.parse_links)  


    def parse_content(self, response):
        title = response.css('div h3::text').extract_first().lstrip().rstrip()
        summary = response.css('div.ndcontent.ndb p::text').extract()
        content = response.css('div.ndcontent p::text').extract()
        content.pop(0)
        cat = response.css('ul.breadcrumb > li:nth-child(2) > a span::text').extract_first()
        date = response.css('div.icon_date_top > div.pull-left::text').extract_first()
        content = '\n'.join(content).lstrip().rstrip()
        summary = '\n'.join(summary).lstrip().rstrip()
        yield {'_id': response.url, 'date': date, 'title': title, 'summary': summary, 'content': content, 'type': cat}
