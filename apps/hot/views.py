import requests
from lxml import etree
from rest_framework.response import Response
from rest_framework.views import APIView

from source_code.settings.conf import FICTION_HOT_URL, FICTION_HEADERS


class HotView(APIView):  # 热搜视图，爬取百度风云榜实时数据
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # 添加超类调用
        self.url = FICTION_HOT_URL
        self.headers = FICTION_HEADERS

    # 未登录也可以显示热搜，因此禁用drf帮我们做的认证
    def perform_authentication(self, request):
        pass

    def get_page(self):  # 爬取百度风云榜小说热搜页面
        html = requests.get(url=self.url, headers=self.headers)
        return html.content.decode('gb2312')

    def get(self, request):
        html = etree.HTML(self.get_page())
        li_list = html.xpath('//*[@id="main"]/div[2]/div[2]/div/div/div/ul/li')  # 获取页面榜单的li列表
        data = []
        for book in li_list:
            book_name = book.xpath('./div[1]/a[1]/@title')  # 获取热搜书名,xpath获取为list类型
            if book_name:  # 判断是否获取到数据
                data.append({'book_name': book_name})
        return Response({
            'errno': 0,
            'errmsg': 'OK',
            'data': data
        })