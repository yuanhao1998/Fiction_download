FICTION_HOT_URL = "http://top.baidu.com/category?c=10"  # 百度风云榜小说热搜

FICTION_SEARCH = 'http://127.0.0.1:8000/search/?book_name='  # 搜索链接

FICTION_WEBSITE = {  # 网站源
    'www.shuquge.com': 'http://www.shuquge.com/search.php',  # 书趣阁
    'www.booktxt.net/': 'https://www.booktxt.net/',  # 顶点小说
    'www.biquge.info': 'http://www.biquge.info/',  # 笔趣阁
}

FICTION_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/84.0.4147.105 Safari/537.36 ',
}


SCRAPYD_SCHEDULE = 'http://localhost:6800/schedule.json'  # scrapyd调度地址
