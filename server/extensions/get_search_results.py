import json
import random
import traceback

import requests
from bs4 import BeautifulSoup


class SearchFetcher(object):

    """
    从搜狗搜索中抓取搜索结果。

    不需要 COOKIE。
    """
    
    source = ["sougou_wenwen", "sougou_zhihu"]
    
    
    @staticmethod
    def fetch_sougou_wenwen_results(
        query
    ):
        """
        抓取搜狗问问的搜索结果。

        Args:
            query (_type_): _description_
        """
        query = '+'.join(query.split(' '))
        url = f'https://www.sogou.com/sogou?query={query}&cid=&s_from=result_up&insite=wenwen.sogou.com'

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
        soup = BeautifulSoup(
            response.text, 
            'html.parser'
        )

        all_search_results = []
        div_contents = soup.find_all(class_='vrwrap')

        for div_content in div_contents:
            cur_result = {}
            a_tag = div_content.find('a')
            if a_tag:
                cur_result['title'] = a_tag.get_text().strip()
                
            span_tag = div_content.find('p', class_='star-wiki')
            if span_tag:
                cur_result['body'] = span_tag.get_text().strip().replace('最佳答案', '').strip()
            
            if 'title' in cur_result and 'body' in cur_result:
                all_search_results.append(cur_result)
                
        return all_search_results
    
    @staticmethod
    def test_fetch_sougou_wenwen_results():
        """
        测试 fetch_sougou_wenwen_results 方法。
        """
        res = SearchFetcher.fetch_sougou_wenwen_results(
            "胡静 个人生活"
        )
        return res != []
    
    @staticmethod
    def fetch_sougou_zhihu_results(
        query
    ):
        """
        抓取搜狗搜索中知乎的结果。

        Args:
            query (_type_): _description_
        """
        query = '+'.join(query.split(' '))
        url = f'https://www.sogou.com/sogou?pid=sogou-wsse-ff111e4a5406ed40&insite=zhihu.com&query={query}'

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
        soup = BeautifulSoup(
            response.text, 
            'html.parser'
        )

        all_search_results = []
        div_contents = soup.find_all(class_='vrwrap')

        for div_content in div_contents:
            cur_result = {}
            a_tag = div_content.find('a')
            if a_tag:
                cur_result['title'] = a_tag.get_text().strip()
                
            span_tag = div_content.find('p', class_='star-wiki')
            if span_tag:
                cur_result['body'] = span_tag.get_text().strip().replace('最佳答案', '').strip()
            
            if 'title' in cur_result and 'body' in cur_result:
                all_search_results.append(cur_result)
                
        return all_search_results

    
    @staticmethod
    def test_fetch_sougou_zhihu_results():
        """
        测试 fetch_sougou_zhihu_results 方法。
        """
        res = SearchFetcher.fetch_sougou_zhihu_results(
            "胡静 个人生活"
        )
        return res != []
    
    @staticmethod
    def fetch_search_results(query):
        """
        获取搜索结果。
        """
        all_results = []
        
        if 'sougou_wenwen' in SearchFetcher.source:
            try:
                all_results.extend(
                    SearchFetcher.fetch_sougou_wenwen_results(query)
                )
            except Exception as e:
                print(f"Error in fetch_sougou_wenwen_results: {e}")
                traceback.print_exc()
        
        if 'sougou_zhihu' in SearchFetcher.source:
            try:
                all_results.extend(
                    SearchFetcher.fetch_sougou_zhihu_results(query)
                )
            except Exception as e:
                print(f"Error in fetch_sougou_zhihu_results: {e}")
                traceback.print_exc()
        
        if all_results:
            random.shuffle(all_results)
        
        return all_results
        
        
if __name__ == '__main__':
    print(
        json.dumps(
            SearchFetcher.fetch_search_results("胡静 个人生活"), 
            ensure_ascii=False, 
            indent=4
        )
    )