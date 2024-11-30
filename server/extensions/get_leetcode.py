import json
import traceback

import requests


class LeetCodeFetcher(object):
    
    """
    从「力扣」抓取题目数据。

    COOKIE 获取 URL: https://leetcode.cn/studyplan/top-100-liked/
                    https://leetcode.com/studyplan/top-100-liked/
    """
    
    CN_CSRF_TOKEN = "l8UgYstBLS5z2GIo3pCYvOukhHt6QkDgV7hiP6QLjskM9lQBtcOzkHjENFq29LF2"
    CN_COOKIE = "aliyungf_tc=a77b5475e8e591c3c9bc332f14dc3406c898f5fc65469c75f2cfaf702405ea24; gr_user_id=a69c0bf3-8de3-4acc-8076-919daf3d3aab; Hm_lvt_f0faad39bcf8471e3ab3ef70125152c3=1731935412; HMACCOUNT=5B8BB6655D5A3929; _bl_uid=Iqmwb3Upn7O1Rmn4U9X4jmRzCtg2; messages=W1siX19qc29uX21lc3NhZ2UiLDAsMjUsIlx1NjBhOFx1NWRmMlx1N2VjZlx1NzY3Ylx1NTFmYSJdXQ:1tD1Xf:wQv_pMs8SQKKUSuPgtt47KLqTsFSZSC0c82BfIPN-n0; csrftoken=l8UgYstBLS5z2GIo3pCYvOukhHt6QkDgV7hiP6QLjskM9lQBtcOzkHjENFq29LF2; tfstk=f5BsBUDm_ZBUZsNaNmEeRRhXPfvbYZwz5mtAqiHZDdpTcx_P2O8aolfBlwT3jOzMQxCfqiY93dWahsTpBIfwuF8Xhib7YzyzUGjMndUzz8RF1YawEqKvXq8Kp30sYJ4YUGjivSUMbryrlyKe7NLAkCdp938KMVQxBMEBDnutMAQYAMLH2hK9MAppJ3-oXKpAkp3p-nhg-5xEcej_YDVs8qa04GTIHYikWCUhfjk-evt9OUdpRxI1dhO6yGBZjYV6c_BWsaUE_FC5ZatP7JH1PGQ1wQBtJy9cY__XVOE-NE_GvORdBolkxKfOwdBbPVId5NXGwGUEOH1db9OFezMXs6QGZI6488vNagWDwOesreRkca9OOyH1ygloUUOAfjiBZxtBzkZIijqEu1pluxgVOCKHYmEQAbkM6HxCskZIijA9xHS3AkGrI; a2873925c34ecbd2_gr_last_sent_cs1=modest_arc; _gid=GA1.2.154759010.1732887832; sl-session=RNFgO8l1TGdVoqIRKzOOnA==; LEETCODE_SESSION=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfYXV0aF91c2VyX2lkIjoiMTc1NTMxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIwMjJiZTY5Y2I2MGM4ZTExMjQ5NmRkNDYyYmM5ZDU4MTNmNDFjMGY0MzIwOWJiNDJmZjM5MWU0NWNiNTNlNWI0IiwiaWQiOjE3NTUzMSwiZW1haWwiOiIiLCJ1c2VybmFtZSI6Ik1vZGVzdF9BUkMiLCJ1c2VyX3NsdWciOiJtb2Rlc3RfYXJjIiwiYXZhdGFyIjoiaHR0cHM6Ly9hc3NldHMubGVldGNvZGUuY24vYWxpeXVuLWxjLXVwbG9hZC91c2Vycy9tb2Rlc3RfYXJjL2F2YXRhcl8xNjU4NTA4NjY0LnBuZyIsInBob25lX3ZlcmlmaWVkIjp0cnVlLCJkZXZpY2VfaWQiOiJlNWY2OGIzMmZhNjhkNjYwOTNjY2M0ZGE4NTE0YWYyMyIsImlwIjoiMTIwLjI0NC4yMzcuNDIiLCJfdGltZXN0YW1wIjoxNzMxOTM1NTI5Ljk0NjgwOTgsImV4cGlyZWRfdGltZV8iOjE3MzQ0NjIwMDAsInZlcnNpb25fa2V5XyI6MH0.vV21x8Uj9lQJ2HxgcYZyPQFyX4jkhNMIM-dU6umlaSk; a2873925c34ecbd2_gr_session_id=2ea5d742-0a78-45b4-b4c6-b8f4f4bf78ec; a2873925c34ecbd2_gr_last_sent_sid_with_cs1=2ea5d742-0a78-45b4-b4c6-b8f4f4bf78ec; a2873925c34ecbd2_gr_session_id_sent_vst=2ea5d742-0a78-45b4-b4c6-b8f4f4bf78ec; _ga=GA1.1.1384504653.1731935412; _ga_PDVPZYN3CW=GS1.1.1732977739.11.1.1732977745.54.0.0; Hm_lpvt_f0faad39bcf8471e3ab3ef70125152c3=1732977746; a2873925c34ecbd2_gr_cs1=modest_arc"
    
    HEADERS = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Cookie': CN_COOKIE,
        'Origin': 'https://leetcode.cn',
        'Referer': 'https://leetcode.cn/problems/two-sum/?envType=study-plan-v2&envId=top-100-liked',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'content-type': 'application/json',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'x-csrftoken': CN_CSRF_TOKEN
    }

    @staticmethod
    def run_code_and_get_result(
        question_id: str,
        code: str,
        test_data: list
    ):
        """运行代码并获取结果。

        Args:
            code (str): 执行的代码 -> "class Solution:\n    def twoSum(self, nums: List[int], target: int) -> ..."
            test_data (list): testCase 从 get_question_details() 里面拿 -> [2,7,11,15]\n9\n[3,2,4]\n6\n[3,3]\n6
            
        Returns:
            dict: 返回结果 -> {
                "expected_code_answer": [
                    "[0,1]",
                    "[1,2]",
                    "[0,1]",
                    ""
                ],
                "code_answer": [
                    "1",
                    "1",
                    "1",
                    ""
                ],
                "correct_answer": false
            }
        """
        try:
            data = {
                "lang": "python3",
                "question_id": question_id,
                "typed_code": code,
                "data_input": test_data
            }

            response = requests.post(
                'https://leetcode.cn/problems/two-sum/interpret_solution/', 
                headers=LeetCodeFetcher.HEADERS, 
                json=data
            ).json()
            
            interpret_id = response['interpret_id']

            response = requests.get(
                f'https://leetcode.cn/submissions/detail/{interpret_id}/check/', 
                headers=LeetCodeFetcher.HEADERS
            ).json()
            
            code_exec_result = {
                'expected_code_answer': response['expected_code_answer'],
                'code_answer': response['code_answer'],
                'correct_answer': response['correct_answer'],
            }
        except:
            print(traceback.format_exc())
            code_exec_result = {
                'expected_code_answer': '',
                'code_answer': '',
                'correct_answer': False
            }
        
        # print(json.dumps(code_exec_result, ensure_ascii=False, indent=4))
        return code_exec_result
    
    @staticmethod
    def test_run_code_and_get_result():
        """
        测试 run_code_and_get_result 方法。
        """
        res = LeetCodeFetcher.run_code_and_get_result(
            question_id='1',
            code='class Solution:\n    def twoSum(self, nums: List[int], target: int) -> List[int]:\n        for i in range(len(nums)):\n            for j in range(i+1, len(nums)):\n                if nums[i] + nums[j] == target:\n                    return [i, j]\n        return []',
            test_data='[2,7,11,15]\n9\n[3,2,4]\n6\n[3,3]\n6'
        ) 
        return res['expected_code_answer'] and res['code_answer']
        
    @staticmethod
    def get_leetcode_hot_list():
        """
        获得当前leetcode热门题目。
        
        Returns:
            题目列表 -> [
                {
                    "title": "最长连续序列",
                    "titleSlug": "longest-consecutive-sequence",
                    "question_id": "128",
                    "difficulty": "MEDIUM"
                },
                ...
            ]
        """    
        payload = {
            "query": """
            query studyPlanDetail($slug: String!) {
                studyPlanV2Detail(planSlug: $slug) {
                    slug
                    name
                    highlight
                    staticCoverPicture
                    colorPalette
                    threeDimensionUrl
                    description
                    premiumOnly
                    needShowTags
                    awardDescription
                    defaultLanguage
                    award {
                        name
                        config {
                            icon
                            iconGif
                            iconGifBackground
                        }
                    }
                    relatedStudyPlans {
                        cover
                        highlight
                        name
                        slug
                        premiumOnly
                    }
                    planSubGroups {
                        slug
                        name
                        premiumOnly
                        questionNum
                        questions {
                            translatedTitle
                            titleSlug
                            title
                            questionFrontendId
                            paidOnly
                            id
                            difficulty
                            hasOfficialSolution
                            topicTags {
                                slug
                                name
                            }
                            solutionInfo {
                                solutionSlug
                                solutionTopicId
                            }
                        }
                    }
                }
            }
            """,
            "variables": {"slug": "top-100-liked"},
            "operationName": "studyPlanDetail"
        }

        response = requests.post(
            "https://leetcode.cn/graphql/", 
            headers=LeetCodeFetcher.HEADERS, 
            json=payload
        )
        
        # print(response)
        # print(
        #     json.dumps(
        #         response.json(), 
        #         ensure_ascii=False, 
        #         indent=4
        #     )
        # )
        
        try:
            response = response.json()
            question_groups = response['data']['studyPlanV2Detail']['planSubGroups']
            
            all_question_info_list = [] 
            for group in question_groups:
                questions = group['questions']
                all_question_info_list.extend([
                    {
                        "title": ele["translatedTitle"],
                        "titleSlug": ele["titleSlug"],
                        "question_id": ele["id"],
                        "difficulty": ele["difficulty"]
                    } for ele in questions]
                )
            return all_question_info_list
        except:
            print(traceback.format_exc())
            return []
    
    @staticmethod
    def test_get_leetcode_hot_list():
        """
        测试 get_leetcode_hot_list 方法。
        """
        return LeetCodeFetcher.get_leetcode_hot_list() != []
    
    @staticmethod
    def get_question_details(
        title_slug: str
    ):
        """
        获得题目描述。
        
        Args:
            title_slug: 题目slug，从get_leetcode_hot_list中获取。
            
        Returns:
            题目描述 -> {
                "translatedTitle": "最长连续序列",
                "questionId: "128",
                "translatedContent": "<p>给定一个未排序的整数数组 <code>nums</code> ，找出数字连续的最长序列（不要求序列元素在原数组中连续）的长度。</p>\n\n<p>请你设计并实现时间复杂度为&nbsp;<code>O(n)</code><em> </em>的算法解决此问题。</p>\n\n<p>&nbsp;</p>\n\n<p><strong>示例 1：</strong></p>\n\n<pre>\n<strong>输入：</strong>nums = [100,4,200,1,3,2]\n<strong>输出：</strong>4\n<strong>解释：</strong>最长数字连续序列是 [1, 2, 3, 4]。它的长度为 4。</pre>\n\n<p><strong>示例 2：</strong></p>\n\n<pre>\n<strong>输入：</strong>nums = [0,3,7,2,5,8,4,6,0,1]\n<strong>输出：</strong>9\n</pre>\n\n<p>&nbsp;</p>\n\n<p><strong>提示：</strong></p>\n\n<ul>\n\t<li><code>0 &lt;= nums.length &lt;= 10<sup>5</sup></code></li>\n\t<li><code>-10<sup>9</sup> &lt;= nums[i] &lt;= 10<sup>9</sup></code></li>\n</ul>\n",
                "test_case": "[100,4,200,1,3,2]\n[0,3,7,2,5,8,4,6,0,1]",
                "code_template: "class Solution:\n    def longestConsecutive(self, nums: List[int]) -> int:\n        pass"
            }
        """
        data = {
            "query": """
            query questionTranslations($titleSlug: String!) {
                question(titleSlug: $titleSlug) {
                    translatedTitle
                    translatedContent
                }
            }
            """,
            "variables": {"titleSlug": title_slug},
            "operationName": "questionTranslations"
        }
        
        response = requests.post(
            'https://leetcode.cn/graphql/', 
            headers=LeetCodeFetcher.HEADERS, 
            json=data
        )
        
        data = {
            "query": """
            query consolePanelConfig($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionId
                questionFrontendId
                questionTitle
                enableRunCode
                enableSubmit
                enableTestMode
                jsonExampleTestcases
                exampleTestcases
                metaData
                sampleTestCase
            }
            }
            """,
            "variables": {"titleSlug": title_slug},
            "operationName": "consolePanelConfig"
        }
        
        test_case_response = requests.post(
            'https://leetcode.cn/graphql/', 
            headers=LeetCodeFetcher.HEADERS, 
            json=data
        )
        
        data = {
            "query": """
            query questionEditorData($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionId
                questionFrontendId
                codeSnippets {
                lang
                langSlug
                code
                }
                envInfo
                enableRunCode
                hasFrontendPreview
                frontendPreviews
            }
            }
            """,
            "variables": {"titleSlug": "longest-consecutive-sequence"},
            "operationName": "questionEditorData"
        }
        
        code_snippet_response = requests.post(
            'https://leetcode.cn/graphql/', 
            headers=LeetCodeFetcher.HEADERS, 
            json=data
        )
        
        try:
            resp = response.json()['data']['question']
            test_case_resp = test_case_response.json()
            code_snippet_resp = code_snippet_response.json()
            resp['test_case'] = test_case_resp['data']['question']['exampleTestcases']
            resp['questionId'] = test_case_resp['data']['question']['questionId']
            resp['code_template'] = [ele['code'] for ele in code_snippet_resp['data']['question']['codeSnippets'] if ele['lang']  == 'Python3'][0]
            return resp
        except:
            print(traceback.format_exc())
            return {}
        
    @staticmethod
    def test_get_question_details():
        """
        测试 get_question_details 方法。
        """
        return LeetCodeFetcher.get_question_details(
            'two-sum'
        ) != {}
        

if __name__ == '__main__':
    print(
        json.dumps(
            LeetCodeFetcher.get_leetcode_hot_list(),
            ensure_ascii=False,
            indent=4
        )
    )
    
    # print(
    #     json.dumps(
    #         LeetCodeFetcher.get_question_details(
    #             'two-sum'
    #         ),
    #         ensure_ascii=False,
    #         indent=4
    #     )
    # )
    
    # print(
    #     LeetCodeFetcher.run_code_and_get_result(
    #         question_id='1',
    #         code='class Solution:\n    def twoSum(self, nums: List[int], target: int) -> List[int]:\n        for i in range(len(nums)):\n            for j in range(i+1, len(nums)):\n                if nums[i] + nums[j] == target:\n                    return [i, j]\n        return []',
    #         test_data='[2,7,11,15]\n9\n[3,2,4]\n6\n[3,3]\n6'
    #     )
    # )