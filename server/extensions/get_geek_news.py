# !/usr/bin/env python3
import json
import traceback
from datetime import datetime

import requests
from bs4 import BeautifulSoup


class GeekNewsFetcher(object):
    
    """
    从「稀土掘金上」抓取新闻数据。

    COOKIE 获取 URL: https://juejin.cn/
    """
    
    CSRF = "000100000001fd0975a4bac60bac97094fc470633c985b85f935a7ef6f7fa8c77e072c8421fc1808c682752a28d3"
    COOKIE = "_tea_utm_cache_2608=undefined; __tea_cookie_tokens_2608=%257B%2522user_unique_id%2522%253A%25227303887821520356876%2522%252C%2522web_id%2522%253A%25227303887821520356876%2522%252C%2522timestamp%2522%253A1713608288581%257D; csrf_session_id=db8fb4e5e2eb82d9dbafd21c032aa0d4"
    
    @staticmethod
    def fetch_geek_news(
        article_id: str
    ):
        """解析出具体 url 中的内容。

        Args:
            article_id (str): _description_
        """
        url = f'https://juejin.cn/post/{article_id}'
        headers = {
            'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Referer': 'https://mini.eastday.com/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        response = requests.get(url, headers=headers, verify=False)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        title_div = soup.find(class_='article-title')
        title = title_div.get_text().strip() if title_div else ""

        name_span = soup.find(class_='name')
        name = name_span.get_text().strip() if name_span else ""

        time_span = soup.find(class_='time')
        time = time_span.get_text().strip() if time_span else ""

        article = ""
        div_contents = soup.find_all('div', class_='article-viewer markdown-body result')
        for div_content in div_contents:
            article += div_content.get_text().lstrip()
            
        article_dict = {
            'title': title,
            'name': name,
            'time': time,
            'content': article
        }
        
        return article_dict
    
    @staticmethod
    def test_fetch_geek_news():
        """
        测试 fetch_geek_news 方法。
        """
        res = GeekNewsFetcher.fetch_geek_news(
            '7438124226501459968'
        )
        return res['content'] or res['title']
        
    @staticmethod
    def fetch_hot_list():
        """
        抓取当前稀土掘金上的热门文章列表。
        """
        url = 'https://api.juejin.cn/recommend_api/v1/article/recommend_all_feed'

        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'cookie': GeekNewsFetcher.COOKIE,
            'origin': 'https://juejin.cn',
            'priority': 'u=1, i',
            'referer': 'https://juejin.cn/',
            'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            'x-secsdk-csrf-token': GeekNewsFetcher.CSRF
        }

        data = {
            "id_type": 2,
            "client_type": 2608,
            "sort_type": 300,
            "cursor": "0",
            "limit": 20
        }

        try:
            response = requests.post(url, headers=headers, json=data).json()
            return [{
                'id': ele['item_info']['article_id'],
                'title': ele['item_info']['article_info']['title'],
                'abstract': ele['item_info']['article_info']['brief_content'],
                'publisher': ele['item_info']['author_user_info']['user_name'],
                'publisher_avatar_url': ele['item_info']['author_user_info']['avatar_large'],
                'tags': [tag['tag_name'] for tag in ele['item_info']['tags']],
                'publish_time': datetime.fromtimestamp(
                    int(ele['item_info']['article_info']['ctime'])
                    ).strftime('%Y-%m-%d %H:%M:%S'),
                'read_count': ele['item_info']['article_info']['view_count'],
                'read_time': ele['item_info']['article_info']['read_time'],
            } for ele in response['data']]
        except:
            print(traceback.format_exc())
            return []
        
    @staticmethod
    def test_fetch_hot_list():
        """
        测试 fetch_geek_news 方法。
        """
        return GeekNewsFetcher.fetch_hot_list() != []
        

if __name__ == '__main__':
    # print(
    #     json.dumps(
    #         GeekNewsFetcher.fetch_hot_list(),
    #         ensure_ascii=False,
    #         indent=4
    #     )
    # )
    
    print(
        json.dumps(
            GeekNewsFetcher.fetch_geek_news(
                '7440830008123228212'
            ),
            ensure_ascii=False,
            indent=4
        )
    )