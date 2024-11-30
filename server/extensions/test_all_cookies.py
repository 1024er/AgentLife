"""
测试所有的 cookie 是否失效。
"""
from tqdm import tqdm
from extensions.get_geek_news import GeekNewsFetcher
from extensions.get_news import NewsFetcher
from extensions.get_search_results import SearchFetcher
from extensions.get_leetcode import LeetCodeFetcher
from extensions.post_weibo import WeiBoTools


TEST_CLASSES = [
    GeekNewsFetcher,
    NewsFetcher,
    SearchFetcher,
    LeetCodeFetcher,
    WeiBoTools
]

def test_all_cookies():
    """
    测试所有 cookie。
    """
    total_num, err_num = 0, 0
    for test_cls in tqdm(TEST_CLASSES, desc="Testing cookies..."):
        for method_name in dir(test_cls):
            if method_name.startswith('test_'):
                method = getattr(test_cls, method_name)
                try:
                    assert method()
                    print(f'[✅ Passed] {test_cls.__name__}.{method_name}')
                except Exception as e:
                    print(f'[❌ Unpassed] {test_cls.__name__}.{method_name}')
                    err_num += 1
                total_num += 1
    
    print(f"Pass Rate: {(total_num - err_num) / total_num * 100:.2f}%({total_num - err_num}/{total_num}).")
    
    
if __name__ == '__main__':
    test_all_cookies()