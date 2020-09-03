from urllib.parse import urlparse

from lxml import etree
from lxml.html import tostring
from rest_framework.response import Response
from rest_framework.views import APIView

from source_code.settings.conf import FICTION_WEBSITE, FICTION_HEADERS
from utils.page_url import get_page, post_page


class BookSearchView(APIView):  # 返回搜索书籍的结果
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.url = list(FICTION_WEBSITE.values())[0]
        self.headers = FICTION_HEADERS

    # 未登录也可以显示热搜，因此禁用drf帮我们做的认证
    def perform_authentication(self, request):
        pass

    def get(self, request, book_name):  # 返回搜索到的内容
        if not book_name:  # 校验是否获取到参数
            return Response({
                'errno': 4103,
                'errmsg': 'missing important parameter'
            })
        response = post_page(url=self.url, headers=self.headers, data={'searchkey': book_name})  # post方法获取页面
        html = etree.HTML(response)
        book_list = html.xpath('//div[@class="bookbox"]')  # 开始处理页面数据
        parse_data = urlparse(self.url)  # 解析url地址，用于获取域名
        host = parse_data.scheme + '://' + parse_data.netloc
        data = {}
        temp_list = []
        for book in book_list:
            name = book.xpath('./div/div/h4/a/text()')
            href = host + book.xpath('./div/div/h4/a/@href')[0]  # 将页面获取的url补齐
            tag = book.xpath('./div/div/div[@class="cat"]/text()')
            author = book.xpath('./div/div/div[@class="author"]/text()')
            update = book.xpath('./div/div/div[@class="update"]/a/text()')
            if book_name:
                temp = {
                    'name': name[0], 'href': href, 'tag': tag[0],
                    'author': author[0], 'update': update[0]
                }
                temp_list.append(temp)
        data[self.url] = temp_list
        return Response({
            'errno': 0,
            'errmsg': 'OK',
            'data': data
        })


class BookSearchDetailView(APIView):  # 获取查询书籍的详情

    # 未登录也可以显示热搜，因此禁用drf帮我们做的认证
    def perform_authentication(self, request):
        pass

    def get(self, request, *args, **kwargs):
        href = request.query_params.get('href')
        response = get_page(url=href)  # get方法获取页面
        html = etree.HTML(response)
        data = tostring(html.xpath('//div[@class="info"]')[0]).decode()
        return Response({
            'errno': 0,
            'errmsg': 'OK',
            'data': data
        })