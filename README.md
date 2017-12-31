# SearchOnline [基于Python3.5，其他python版本未测试]
实现搜索引擎搜索内容回传以及制定URL内容加载回传，适合作为远程插件功能使用。

## 使用方法
* 安装Python 依赖库：`pip install -r requirements.txt`
* 搜索功能：
    ```python 
    searchResults=WebPageOnlineEngine.search("习大大",search_engines=["baidu"],num_pages_for_keyword=1)
    print(json.dumps(searchResults,indent=4,ensure_ascii=False))
    ```
    结果输出：
    
    ```json
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
    ```
* 加载页面内容功能：
    ```python
    urls = [
            "https://arxiv.org/pdf/1710.00811.pdf",
            'http://blog.csdn.net/nero_g/article/details/52912305',
            'https://gss1.bdstatic.com/9vo3dSag_xI4khGkpoWK1HF6hhy/baike/c0%3Dbaike150%2C5%2C5%2C150%2C50/sign=c05506e79482d158af8f51e3e16372bd/c2fdfc039245d688c56332adacc27d1ed21b2451.jpg'
        ]
        for url in urls:
            urlData = WebPageOnlineEngine.get_url_content(url)
            print(json.dumps(urlData,indent=4,ensure_ascii=False))
    ```
    
    输出结果：
    
    ```json
    {
        "file_extension": ".htm",   //URL对应的文件类型
        "error": 0,       //错误码，0-表示正常，其他表示出现错误
        "error_msg": "",   //若出现错误，错误消息内容
        "url": "http://blog.csdn.net/nero_g/article/details/52912305",  //加载内容原始URL地址
        "b64_data": "Cgo8IURPQ1RZU....==",     //URL对应内容base64编码字符串，需要对应解码
        "content_type_origin": "text/html; charset=utf-8",    //原始URL请求Response　Header头部原始Content-Type类型
        "time": 1514717424,    //内容返回处理的时间戳
        "content_type": "text/html",     //原始URL请求Response　Header头部Content-Type   内容类型，不含其他附加值
        "status": 200   //URL访问返回的Http Status Code
    }
    ```
* 完整代码参考 `web_page_online.py`

