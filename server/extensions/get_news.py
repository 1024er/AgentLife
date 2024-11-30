"""
调用各种新闻 API，获取新闻数据。
"""
import json
import time
import random
import traceback
from datetime import datetime

import requests
from bs4 import BeautifulSoup


class NewsFetcher(object):

    """
    从各种新闻 API 获取新闻数据。

    东方资讯新闻 COOKIE 获取 URL: https://mini.eastday.com/
    """
    
    news_pool = []
    last_fetch_time = None
    news_source = ["toutiao", "dongfang"]
    COOKIE = "search_qid=02263; vqid_key=qid02650; mylist=%7B%22uid%22%3A%2217313065912560026%22%2C%22softtype%22%3A%22minins%22%2C%22softname%22%3A%22DFZX-LITE-MININS%22%7D; ..."
    
    @staticmethod
    def fetch_toutiao_news():
        """
        获取今日头条新闻。
        """
        api_url = 'http://is.snssdk.com/api/news/feed/v51/'
        response = requests.get(api_url).json()
        contents = [json.loads(content["content"]) for content in response['data']]
        
        parsed_contents = [
            NewsFetcher.parse_toutiao_api_resposne(content) for content in contents
        ]
        return [c for c in parsed_contents if c]
    
    @staticmethod
    def test_fetch_toutiao_news():
        """
        测试 fetch_toutiao_news 方法。
        """
        res = NewsFetcher.fetch_toutiao_news()
        return len(res) > 0
    
    @staticmethod
    def fetch_dongfang_news():
        """
        获取东方资讯新闻。
        """
        def get_all_hot_news():
            """
            获取当前所有的热点新闻列表。
            """
            root_url = 'https://mini.eastday.com'
            url = f'{root_url}/ns/api/index/merge/index-merge.json?callback=indexMerge&_=1731316854559'
            
            headers = {
                'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
                'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                'Connection': 'keep-alive',
                'Cookie': NewsFetcher.COOKIE,
                'Referer': 'https://mini.eastday.com/',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'
            }

            response = requests.get(url, headers=headers, verify=False).text
            response = response.replace('indexMerge(', '').replace(')', '')
            response = json.loads(response)
            
            all_news = []
            for news in response['top50']:
                news_dict = {
                    'title': news.get('topic', ''),
                    'url': root_url + news.get('url', '') if news.get('url', '') else '',
                    'publish_time': datetime.fromtimestamp(news.get('date', '')).strftime('%Y-%m-%d %H:%M:%S') if news.get('date', '') else '未知',
                    'publisher_name': news.get('source', '未知'),
                    'read_count': '未知'
                }
                all_news.append(news_dict)
                
            for n_dict in response['qdYuleSlider']:
                for news in n_dict['data']:
                    news_dict = {
                        'title': news.get('topic', ''),
                        'url': root_url + news.get('url', '') if news.get('url', '') else '',
                        'publish_time': '未知',
                        'publisher_name': '未知',
                        'read_count': '未知'
                    }
                    all_news.append(news_dict)
            
            return all_news

        def fetch_content(news):
            """抓取指定 url 的具体内容，包含作者、发布时间、正文等。

            Args:
                news (dict): _description_
            """
            if not news.get('url', ''):
                print(f"No url found in news: {news}")
                news['content'] = ""
                return news
            
            url = news['url']
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, verify=False)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            div_content = soup.find(id='J-contain_detail_cnt')
            if div_content:
                news['content'] = div_content.get_text()
            
            title_detail_div = soup.find('div', class_='J-title_detail title_detail')
            fl_divs = title_detail_div.find_all('div', class_='fl')[0].find_all('i')
            
            if fl_divs:
                news['publish_time'] = fl_divs[0].get_text()
                news['publish_author'] = fl_divs[1].get_text()
            
            return news
        
        all_news = get_all_hot_news()
        all_news = [fetch_content(news) for news in all_news]
        return all_news

    @staticmethod
    def test_fetch_dongfang_news():
        """
        测试 fetch_dongfang_news 方法。
        """
        res = NewsFetcher.fetch_dongfang_news()
        return len(res) > 0
    
    @staticmethod
    def parse_toutiao_api_resposne(
        content: dict
    ):
        """
        解析今日头条API返回的数据。
        """
        try:
            if "meida_info" in content:
                publisher_avatar_url = content["media_info"].get("avatar_url", "")
                publisher_name = content["media_info"].get("name", "")
            elif "user_info" in content:
                publisher_avatar_url = content["user_info"].get("avatar_url", "")
                publisher_name = content["user_info"].get("name", "")
            elif "user" in content:
                publisher_avatar_url = content["user"].get("avatar_url", "")
                publisher_name = content["user"].get("name", "")
                
            if "feed_title" in content:
                content_title = content["feed_title"]
            elif "title" in content:
                content_title = content["title"]
            elif "share_info" in content:
                content_title = content["share_info"].get("title", "")
            
            publish_time_timestamp = content.get("publish_time", "")
            publish_time = datetime.fromtimestamp(publish_time_timestamp).strftime("%Y-%m-%d %H:%M:%S") if publish_time_timestamp else ""
            
            content_abstract = content.get("abstract", "")
            
            if (
                content_abstract
                and
                '习近平' not in content_title
            ):
                return {
                    "title": content_title,
                    "content": content_abstract,
                    "publish_time": publish_time,
                    "read_count": content.get("read_count", 0),
                    "publisher_name": publisher_name,
                    "publisher_avatar_url": publisher_avatar_url,
                }
            else:
                return {}
            
        except:
            print(traceback.format_exc())
            return {}

    @staticmethod
    def fetch_news(
        num: int = 4
    ) -> list:
        """随机获取当前最新的 num 条新闻。

        Args:
            num (int, optional): _description_. Defaults to 4.

        Returns:
            list: news list -> [
                {
                    "content_title": content_title,
                    "content_abastract": content_abstract,
                    "publish_time": publish_time,
                    "read_count": content.get("read_count", 0),
                    "publisher_name": publisher_name,
                    "publisher_avatar_url": publisher_avatar_url,
                },
                ...
            ]
        """
        if (
            not NewsFetcher.last_fetch_time
            or
            time.time() - NewsFetcher.last_fetch_time > 60 * 60             # 1h 刷新一次
        ):
            start_time = time.time()
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Updating news pool, with {NewsFetcher.news_source}...")
          
            NewsFetcher.news_pool = []
            if "toutiao" in NewsFetcher.news_source:
                NewsFetcher.news_pool += NewsFetcher.fetch_toutiao_news()
                
            if "dongfang" in NewsFetcher.news_source:
                NewsFetcher.news_pool += NewsFetcher.fetch_dongfang_news()
                
            print(f"News pool updated, cost {round(time.time() - start_time, 2)}s, fetched {len(NewsFetcher.news_pool)} news.")
            NewsFetcher.last_fetch_time = time.time()

        return random.sample(NewsFetcher.news_pool, num)
    
    
if __name__ == '__main__':
    while True:
        print(NewsFetcher.fetch_news(num=1))
        input("Press any key to continue...")