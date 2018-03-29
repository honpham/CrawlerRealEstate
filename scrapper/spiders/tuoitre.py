import scrapy


class TuoiTreSpider(scrapy.Spider):
    name = "tuoitre_scrapper"
    path = {'Thoi su/Thoi su': 3,  'Thoi su/Xa hoi': 200003, 'Thoi su/Phong su': 89, 'Thoi su/Nghi': 87,
            'The gioi/The gioi': 2, 'The gioi/Binh luan': 94,  'The gioi/Kieu bao': 312, 'The gioi/Muon mau': 442, 'The gioi/Ho so': 20,
            'Phap luat/Phap luat': 6, 'Phap luat/Chuyen phap dinh': 266, 'Phap luat/Tu van': 79, 'Phap luat/Phap ly': 200005,
            'Kinh doanh/Kinh doanh': 11, 'Kinh doanh/Tai chinh': 86, 'Kinh doanh/Doanh nghiep': 775, 'Kinh doanh/Mua sam': 200006, 'Kinh doanh/Dau tu': 200007,
            'Xe/Xe': 659,
            'Nhip song tre/Nhip song tre': 7, 'Nhip song tre/Xu huong': 200012, 'Nhip song tre/Kham pha': 200013, 'Nhip song tre/Yeu': 194, 'Nhip song tre/Nhan vat': 200014, 'Nhip song tre/Viec lam': 269,
            'Van hoa/Van hoa': 200017, 'Van hoa/Doi song': 200018, 'Van hoa/Van hoa doc sach': 61,
            'Giai tri/Giai tri': 10, 'Giai tri/Am nhac': 58, 'Giai tri/Dien anh': 57, 'Giai tri/TV show': 385, 'Giai tri/Thoi trang': 919, 'Giai tri/Hau truong': 922,
            'Giao duc/Giao duc': 13, 'Giao duc/Hoc duong': 1507, 'Giao duc/Du hoc': 85, 'Giao duc/Cau chuyen giao duc': 913, 'Giao duc/Goc hoc tap':  200020,
            'Khoa hoc/Khoa hoc': 661, 'Khoa hoc/Thuong thuc': 200010, 'Khoa hoc/Phat minh': 200011,
            'Ban doc lam bao/Ban doc lam bao': 118, 'Ban doc lam bao/Duong day nong': 937, 'Ban doc lam bao/Tieu diem': 1360, 'Ban doc lam bao/Chia se': 940}
    root_path = 'http://tuoitre.vn'
    url = root_path + "/timeline/%d/trang-%d.htm"

    def __init__(self):
        self.count = {x: 0 for x in TuoiTreSpider.path}

    def start_requests(self):
        for x in TuoiTreSpider.path:
            yield scrapy.http.Request(url=TuoiTreSpider.url % (TuoiTreSpider.path[x], self.count[x]), callback=self.parse_with_type(x))

    def parse_with_type(self, _type):
        def parse(response):
            paths = response.selector.xpath('//a/@href').extract()
            if paths:
                for path in paths:
                    yield scrapy.http.Request(url=TuoiTreSpider.root_path + path, callback=self.parse_article(_type))
                self.count[_type] += 1
                yield scrapy.http.Request(url=TuoiTreSpider.url % (TuoiTreSpider.path[_type], self.count[_type]), callback=parse)
        return parse

    def parse_article(self, _type):
        def parse(response):
            left_side = response.selector.xpath('//div[@class="left-side"]')
            title = left_side.xpath(
                '//h1[@class="title-2"]/text()').extract()[0].rstrip().lstrip()
            summary = left_side.xpath(
                '//h2[@class="txt-head"]/text()').extract()[0].rstrip().lstrip()
            content = '\n'.join(left_side.xpath(
                '//div[@class="fck"]/p//text()').extract()).lstrip().rstrip()
            date = left_side.xpath('//span[@class="date"]/text()').extract()[0]
            tags = left_side.xpath(
                '//ul[@class="block-key"]/li/a/text()').extract()
            return {'_id': response.url, 'date': date, 'title': title, 'summary': summary, 'content': content, 'type': _type, 'tags': tags}
        return parse
