import scrapy
from random import randint

class VnExpressSpider(scrapy.Spider):
    name = "vnexpress"
    BASE_URL = 'https://vnexpress.net' 

    def start_requests(self):
        url = self.BASE_URL
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        links = response.css('#main_menu a::attr(href)') .extract()
        normal_links = [self.BASE_URL + x for x in links if not x.startswith('http') and "raovat" not in x and "video" not in x]
        full_links = [x for x in links if x.startswith('http')]
        links = normal_links + full_links
        print(links)
        for link in links:
            yield scrapy.Request(link, callback=self.parse_links)
        
    def parse_links(self, response):
        links = response.css('article .title_news a::attr(href)').extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_content)
        paging = response.css('#pagination a.next::attr(href)').extract_first()
        if paging:
            yield scrapy.Request(paging, callback=self.parse_links)        

    def parse_content(self, response):
        title = response.css('.title_news_detail::text').extract_first().lstrip().rstrip()
        summary = response.css('.sidebar_1 .description::text').extract()
        content = response.css('.content_detail p').xpath('.//text()').extract()
        cat = response.css('.cat_header ul li.start a::text').extract_first()
        date = response.css('.time::text').extract_first()
        content = '\n'.join(content).lstrip().rstrip()
        summary = '\n'.join(summary).lstrip().rstrip()
        yield {'_id': response.url, 'date': date, 'title': title, 'summary': summary, 'content': content, 'type': cat}

