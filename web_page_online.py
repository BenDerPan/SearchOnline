from GoogleScraper import scrape_with_config, GoogleSearchError
import requests
import json
import os
import datetime
import base64

class WebPageOnlineEngine:
    '''
    网页内容在线处理引擎类，实现搜索引擎搜索以及页面内容获取
    '''
    #所有可选搜索引擎列表
    SUPPORTED_SEARCH_ENGINES_ALL = ['google', 'yandex', 'bing', 'yahoo', 'baidu', 'duckduckgo', 'ask']
    #默认搜索引擎列表
    SUPPORTED_SEARCH_ENGINES_DEFAULT = ['google', 'bing', 'baidu']
    #中国默认可用搜索引擎列表
    SUPPORTED_SEARCH_ENGINES_CHINA = ['bing', 'baidu']
    #URL请求内容类型字典集合
    CONTENT_FILE_TYPES = None

    @staticmethod
    def search(keyword, search_engines=SUPPORTED_SEARCH_ENGINES_CHINA, search_offset=1, num_pages_for_keyword=3):
        '''
        从搜索引擎中搜索相关关键字内容
        :param keyword: 关键字
        :param search_engines: 选择的搜索引擎列表
        :param search_offset: 起始页，1为第一页
        :param num_pages_for_keyword: 选择搜索结果页数
        :return: 搜索得到的结果字典集合
            {
                "baidu": {
                    "query": "习大大",
                    "pages": {
                        "1": {
                            "scrape_method": "http",
                            "requested_at": 1514689866,
                            "status": "successful",
                            "num_results_for_query": "搜索工具百度为您找到相关结果约11,300,000个",
                            "links": [
                                {
                                    "rank": 1,
                                    "domain": "www.baidu.com",
                                    "title": "习大大的“亲民范儿”——十三张图告诉你有多“暖暖哒”_央广网",
                                    "snippet": "2015年8月5日 - “亲吻芦山地震灾区男孩”“大雨中挽裤腿自己撑伞”“吃‘红军饭’时给战士夹菜”等一幕幕场景更是全面地让大家领略到了“习大大”朴实亲民的领导风格...",
                                    "visible_link": null,
                                    "link": "http://www.baidu.com/link?url=kkX4cfyK-tCNlwfcdH1T8UHm3lOukNdK55DIpyZTo3O_I1hbAFxzct2cW7B3hw06UiMhkG7_gZMG-1dfF3MyBOdyIOmaSbsBKUsMdtwjMpC"
                                },
                                {
                                    "rank": 2,
                                    "domain": "www.baidu.com",
                                    "title": "被叫“习大大” 总书记笑了_网易财经",
                                    "snippet": "2014年9月10日 - 潘聿航提到,当时牌子的内容有“习总书记辛苦了”和“习大大辛苦了”两个备选。“曾经犹豫了一番,担心用 习大大 这三个字欠妥。”但他们想,总书...",
                                    "visible_link": null,
                                    "link": "http://www.baidu.com/link?url=5tBlgVr6Sj0HZWOBdiSNZx6ls8G6I5ZKOKdfVzQXAQ3Bxn7DQwahn7mTe2CPCRKpRafI5a-ujrYRkxh-Tgyo-K"
                                }
                            ]
                        }
                    },
                    "num_results": 10
                }
            }
        '''
        # See in the config.cfg file for possible values
        config = {
            'use_own_ip': True,
            'keyword': keyword,
            'search_engines': search_engines,
            'num_pages_for_keyword': num_pages_for_keyword,
            'scrape_method': 'http',
            'do_caching': False,
            'search_offset': search_offset,
        }

        try:
            search = scrape_with_config(config)
        except GoogleSearchError as e:
            pass

        resultData = {}
        # let's inspect what we got
        try:
            for serp in search.serps:
                if serp.search_engine_name not in resultData:
                    resultData[serp.search_engine_name] = {}
                    resultData[serp.search_engine_name]['num_results'] = 0
                    resultData[serp.search_engine_name]['query'] = serp.query
                    resultData[serp.search_engine_name]['pages'] = {}
                resultData[serp.search_engine_name]['num_results'] += serp.num_results
                pageData = {}
                pageData['num_results_for_query'] = serp.num_results_for_query
                pageData['requested_at'] = int(serp.requested_at.timestamp())
                pageData['status'] = serp.status
                pageData['scrape_method'] = serp.scrape_method
                pageData['links'] = []
                for link in serp.links:
                    res = {}
                    res['domain'] = link.domain
                    res['rank'] = link.rank
                    res['link'] = link.link
                    res['visible_link'] = link.visible_link
                    res['title'] = link.title
                    res['snippet'] = link.snippet
                    pageData['links'].append(res)

                resultData[serp.search_engine_name]['pages'][serp.page_number] = pageData
        except Exception as e:
            print('[!]在线搜索失败：KeyWord={0},SearchEngines={1},Error:{2}'.format(keyword, search_engines, e))

        return resultData

    @staticmethod
    def load_http_content_types(template_file="content-type.json"):
        '''
        从http headers content-type字典文件中加载content-type及其文件扩展名
        :param template_file: 字典文件名称
        :return:配置内容字典对象
        '''
        if not os.path.exists(template_file):
            print("[!]Error:Template file '{0}' not found !!!!!".format(template_file))
            return None
        with open(template_file, 'r') as f:
            return json.loads(f.read())

    @staticmethod
    def get_url_content(url):
        '''
        获取URL内容
        :param url:需要加载内容的URL地址
        :return:URL访问后得到数据内容json值
            {
                "file_extension": ".htm",   #URL对应的文件类型
                "error": 0,       #错误码，0-表示正常，其他表示出现错误
                "error_msg": "",   #若出现错误，错误消息内容
                "url": "http://blog.csdn.net/nero_g/article/details/52912305",   #加载内容原始URL地址
                "b64_data": "Cgo8IURPQ1RZU....==",     #URL对应内容base64编码字符串，需要对应解码
                "content_type_origin": "text/html; charset=utf-8",    #原始URL请求Response　Header头部原始Content-Type类型
                "time": 1514717424,    #内容返回处理的时间戳
                "content_type": "text/html",     #原始URL请求Response　Header头部Content-Type   内容类型，不含其他附加值
                "status": 200    #URL访问返回的Http Status Code
            }
        '''
        url = url.strip()
        if not WebPageOnlineEngine.CONTENT_FILE_TYPES:
            WebPageOnlineEngine.CONTENT_FILE_TYPES = WebPageOnlineEngine.load_http_content_types()
        base_file_name = os.path.basename(url)
        status_code = -1
        error = 0
        error_msg = ''
        content_type = ""
        content_type_origin = ""
        extension = "unknown"
        b64Data = ""
        try:
            res = requests.get(url)
            status_code = res.status_code
            content_type_origin = res.headers['Content-Type'].lower()
            content_type = content_type_origin.split(";", maxsplit=1)[0].strip()

            if content_type in WebPageOnlineEngine.CONTENT_FILE_TYPES:
                if "." in base_file_name:
                    parts = base_file_name.rsplit(".", maxsplit=1)
                    if len(parts[1]) < 1:
                        extension = WebPageOnlineEngine.CONTENT_FILE_TYPES[content_type]['default']
                    else:
                        extension = ".{0}".format(parts[1])
                        if extension not in WebPageOnlineEngine.CONTENT_FILE_TYPES[content_type]['file_types']:
                            extension = WebPageOnlineEngine.CONTENT_FILE_TYPES[content_type]['default']
                else:
                    extension = WebPageOnlineEngine.CONTENT_FILE_TYPES[content_type]['default']
            b64Data = base64.b64encode(res.content).decode()
        except Exception as e:
            error = 1
            error_msg = "{}".format(e)

        resultJson = {}
        resultJson['url'] = url
        resultJson['status'] = status_code
        resultJson['error'] = error
        resultJson['error_msg'] = error_msg
        resultJson['content_type'] = content_type
        resultJson['content_type_origin'] = content_type_origin
        resultJson['file_extension'] = extension
        resultJson['time'] = int(datetime.datetime.now().timestamp())
        resultJson['b64_data'] = b64Data
        return resultJson


if __name__ == '__main__':
    searchResults=WebPageOnlineEngine.search("习大大",search_engines=["baidu"],num_pages_for_keyword=1)
    print(json.dumps(searchResults,indent=4,ensure_ascii=False))

    urls = [
        "https://arxiv.org/pdf/1710.00811.pdf",
        'http://blog.csdn.net/nero_g/article/details/52912305',
        'https://gss1.bdstatic.com/9vo3dSag_xI4khGkpoWK1HF6hhy/baike/c0%3Dbaike150%2C5%2C5%2C150%2C50/sign=c05506e79482d158af8f51e3e16372bd/c2fdfc039245d688c56332adacc27d1ed21b2451.jpg'
    ]
    for url in urls:
        urlData = WebPageOnlineEngine.get_url_content(url)
        print(json.dumps(urlData,indent=4,ensure_ascii=False))
