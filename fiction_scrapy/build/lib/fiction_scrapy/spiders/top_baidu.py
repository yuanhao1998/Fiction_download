import scrapy


class TopBaiduSpider(scrapy.Spider):
    name = 'top_baidu'
    allowed_domains = ['top.baidu.com']
    start_urls = ['http://top.baidu.com/category?c=10/']

    def parse(self, response, **kwargs):
        li_list = response.xpath('//*[@id="main"]/div[2]/div[2]/div/div/div/ul/li')  # 获取页面榜单的li列表
        data = []
        for book in li_list:
            book_name = book.xpath('./div[1]/a[1]/@title')  # 获取热搜书名,xpath获取为list类型
            if book_name:  # 判断是否获取到数据
                temp = {'book_name': book_name, 'href': book_name[0]}
                data.append(temp)
        for value in data:
            print(value)