import scrapy


class ZingSpider(scrapy.Spider):
    name = "zing_scrapper"
    path = {'Thời sự/Giao thông': 'giao-thong', 'Thời sự/Thời sự': 'thoi-su', 'Thời sự/Đô thị': 'do-thi', 'Thời sự/Đời sống': 'doi-song', 'Thời sự/Quốc phòng': 'quoc-phong',
            'Thế giới/Thế giới': 'the-gioi', 'Thế giới/Quân sự': 'quan-su-the-gioi', 'Thế giới/Tư liệu': 'tu-lieu-the-gioi', 'Thế giới/Phân tích': 'phan-tich-the-gioi', 'Thế giới/Người Việt 4 phương': 'nguoi-viet-4-phuong',
            'Kinh doanh/Kinh doanh': 'kinh-doanh-tai-chinh', 'Kinh doanh/Tài chính': 'tai-chinh', 'Kinh doanh/Chứng khoán': 'chung-khoan', 'Kinh doanh/Bất động sản': 'bat-dong-san', 'Kinh doanh/Doanh nhân': 'doanh-nhan',
            'Pháp luật/Pháp luật': 'phap-luat', 'Pháp luât/Pháp đình': 'phap-dinh', 'Pháp luật/Vụ án': 'vu-an',
            'Xuất bản/Xuất bản': 'xuat-ban', 'Xuất bản/Tin tức xuất bản': 'tin-tuc-xuat-ban', 'Xuất bản/Sách hay': 'sach-hay', 'Xuất bản/Tác giả': 'tac-gia',
            'Thể thao/Thể thao': 'the-thao', 'Thể thao/Thể thao Việt Nam': 'the-thao-viet-nam', 'Thể thao/Cúp châu Âu': 'cup-chau-au', 'Thể thao/Thể thao thế giới': 'the-thao-the-gioi', 'Thể thao/Bóng đá': 'bong-da', 'Thể thao/Bóng đá Anh': 'bong-da-anh', 'Thể thao/Bóng đá Việt Nam': 'bong-da-viet-nam', 'Thể thao/Bóng rổ': 'bong-ro', 'Thể thao/Hậu trường thể thao': 'hau-truong-the-thao',
            'Công nghệ/Công nghệ': 'cong-nghe', 'Công nghệ/Điện thoại': 'dien-thoai', 'Công nghệ/Máy tính bảng': 'may-tinh-bang', 'Công nghệ/Ứng dụng di động': 'ung-dung-di-dong',
            'Xe/Xe': 'o-to-xe-may', 'Xe/Xe máy': 'xe-may', 'Xe/Ô tô': 'o-to', 'Xe/Xe độ': 'xe-do', 'Xe/Siêu xe': 'sieu-xe',
            'Giải trí/Giải trí': 'giai-tri', 'Giải trí/Sao Việt': 'sao-viet', 'Giải trí/Sao châu Á': 'sao-chau-a', 'Giải trí/Sao Hollywood': 'sao-hollywood',
            'Âm nhạc/Âm nhạc': 'am-nhac', 'Âm nhạc/Nhạc Việt': 'nhac-viet', 'Âm nhạc/Nhạc Hàn': 'nhac-han', 'Âm nhạc/Nhạc Âu Mỹ': 'nhac-au-my',
            'Phim ảnh/Phim ảnh': 'phim-anh', 'Phim ảnh/Phim chiếu rạp': 'phim-chieu-rap', 'Phim ảnh/Phim truyền hình': 'phim-truyen-hinh', 'Phim ảnh/Game show': 'game-show',
            'Thời trang/Thời trang': 'thoi-trang', 'Thời trang/Thời trang sao': 'thoi-trang-sao', 'Thời trang/Mặc đẹp': 'mac-dep', 'Thời trang/Làm đẹp': 'lam-dep',
            'Sống trẻ/Sống trẻ': 'song-tre', 'Sống trẻ/Gương mặt trẻ': 'guong-mat-tre', 'Sống trẻ/Cộng đồng mạng': 'cong-dong-mang', 'Sống trẻ/Sự kiện': 'su-kien',
            'Giáo dục/Giáo dục': 'giao-duc', 'Giáo dục/Tư vấn': 'tu-van-giao-duc', 'Giáo dục/Du học': 'du-hoc',
            'Sức khỏe/Sức khỏe': 'suc-khoe', 'Sức khỏe/Khỏe đẹp': 'khoe-dep', 'Sức khỏe/Dinh dưỡng': 'dinh-duong', 'Sức khỏe/Mẹ và bé': 'me-va-be', 'Sức khỏe/Bệnh thường gặp': 'benh-thuong-gap',
            'Du lịch/Du lịch': 'du-lich', 'Du lịch/Địa điểm du lịch': 'dia-diem-du-lich', 'Du lịch/Kinh nghiệm du lịch': 'kinh-nghiem-du-lich', 'Du lịch/Phượt': 'phuot'}
    root_path = 'http://news.zing.vn'
    url = root_path + '/%s/trang%d.html'

    def __init__(self):
        self.count = {x: 0 for x in ZingSpider.path}

    def start_requests(self):
        for x in ZingSpider.path:
            yield scrapy.http.Request(url=ZingSpider.url % (ZingSpider.path[x], self.count[x]), callback=self.parse_with_type(x))

    def parse_with_type(self, _type):
        def parse(response):
            paths = response.selector.xpath(
                '//*[@id="category"]//p[@class="title"]/a/@href').extract()
            if paths:
                for path in paths:
                    yield scrapy.http.Request(url=ZingSpider.root_path + path, callback=self.parse_article(_type))
                self.count[_type] += 1
                yield scrapy.http.Request(url=ZingSpider.url % (ZingSpider.path[_type], self.count[_type]), callback=parse)
        return parse

    def parse_article(self, _type):
        def parse(response):
            title = ' '.join(response.selector.xpath(
                '//h1[@class="the-article-title cms-title"]//text()').extract()).lstrip().rstrip()
            summary = ' '.join(response.selector.xpath(
                '//p[@class="the-article-summary cms-desc"]//text()').extract()).lstrip().rstrip()
            content = '\n'.join(response.selector.xpath(
                '//div[@class="the-article-body cms-body"]/p//text() | //div[@class="the-article-body cms-body"]/h3//text()').extract()).lstrip().rstrip()
            date = ' '.join(response.selector.xpath(
                '//li[@class="the-article-publish cms-date"]//text()').extract()).lstrip().rstrip()
            return {'_id': response.url, 'date': date, 'title': title, 'summary': summary, 'content': content, 'type': _type}
        return parse
