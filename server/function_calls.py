import re
import abc
import time
import copy
import inspect
from typing import Any, Dict, List

from utils import (
    distance,
    find_path, 
    get_item_position
)
from llm_utils import LLMClient
from extensions.get_news import NewsFetcher
from extensions.get_books import BooksFetcher
from extensions.get_search_results import SearchFetcher
from extensions.post_weibo import WeiBoTools
from extensions.get_geek_news import GeekNewsFetcher
from extensions.get_leetcode import LeetCodeFetcher


ALL_FUNCTIONS: Dict[str, Dict[str, Any]] = {}   # registry of all functions


class BaseFunctionCall(abc.ABC):
    """
    Function call 抽象基类，该类定义了 call() 用于实现一个具体的逻辑，
    以及 validate_func() 用于判断当前状态是否需要被加入 agent 当前的行为空间中。
    其中，call() 方法必须被子类重写，validate_func() 方法可选重写。
    """
    
    @staticmethod
    @abc.abstractmethod
    def call(*args, **kwargs):
        """
        具体的函数调用实现逻辑，必须在子类中实现。
        """
        pass
    
    @staticmethod
    def validate_func(
        agent_object,
        room
    ):
        """
        用于根据当前状态判断，是否需要被加入 agent 当前的行为空间中，
        若返回 False，则不会被加入，默认返回 True。
        """
        return True
    

def register_function_call_class(
    function_call_obj
):
    """Decorator used to register a function.
    
    ALL_FUNCTIONS Example ->
        {
            "GoTo.call(current_position, target)": "从当前地点出发，前往目标地点，返回规划好的路径点。\n\nArgs:\ncurrent_position (list): 当前位置, e.g. [0, 0]\ntarget (str): 目标地点名称.\n\nReturns:list: 规划路径点, e.g. [[0, 0], [0, 1], [1, 1]]",
            "DoNothing.call()": "什么也不做。",
            ...
        }
    """
    function_name = f"{function_call_obj.__name__}.call({', '.join(inspect.signature(function_call_obj.call).parameters.keys())})"
    ALL_FUNCTIONS[function_name] = {
        "docstring": function_call_obj.call.__doc__,
        "validate_func": function_call_obj.validate_func
    }
    return function_call_obj

# @register_function_call_class
# class Sleep(BaseFunctionCall):
    
#     def call(
#         agent_object: object, 
#         sleep_minute: int
#     ):
#         """开始睡觉。

#         Args:
#             agent_object (object): agent 对象，通常传入 self 即可。
#             sleep_minute (int): 睡眠持续时间，单位为分钟。
#         """
#         agent_object.character['state'] = "sleeping"
        
#         return {
#             "waiting_time": sleep_minute * 60,
#             "emit_message_type": "updateState",
#             "emit_message_value": "sleeping"
#         }

#     def validate_func(
#         agent_object,
#         room
#     ):  
#         all_bed_positions = [
#             item['gridPosition'] for item in room['items'] if 'bed' in item['name']
#         ]
        
#         return any(
#             [
#                 math.dist(agent_object.character['position'], bed_position) <= 1
#                 for bed_position in all_bed_positions
#             ]
#         )


@register_function_call_class
class GoTo(BaseFunctionCall):
    
    def call(
        agent_object: object, 
        target: str
    ):
        """从当前地图中的所有物品中选择一个作为目标地前往。

        Args:
            agent_object (object): agent 对象，通常传入 self 即可。
            target (str): 目标地点名称。
        """
        agent_object.character['state'] = "moving"
        
        target_grid_position = get_item_position(
            agent_object.room['items'], 
            target
        )
        
        if not target_grid_position:
            agent_object.character['event'] = {
                "type": "error",
                "message": f"未找到名为 `{target}` 的地点。"
            }
            return {"waiting_time": 1.0}
        
        path = []
        if target_grid_position['entryGridPosition']:
            cur_target_grid_position = copy.deepcopy(target_grid_position['entryGridPosition'])
            path, _ = find_path(
                agent_object.room,
                agent_object.character['position'],
                cur_target_grid_position
            )
        else:
            for i in range(4):                              # 找到目标 item 附近的一个可落脚的位置
        
                cur_target_grid_position = copy.deepcopy(target_grid_position['gridPosition'])
                
                if i == 0:
                    cur_target_grid_position[0] -= 1
                elif i == 1:
                    cur_target_grid_position[0] += 1
                elif i == 2:
                    cur_target_grid_position[1] -= 1
                else:
                    cur_target_grid_position[1] += 1
                    
                path, _ = find_path(
                    agent_object.room,
                    agent_object.character['position'],
                    cur_target_grid_position
                )
                
                if path:
                    break
                
        if not path:
            print(f"Can not find path from {agent_object.character['position']} -> {target}({target_grid_position})")
            agent_object.character['event'] = {
                "type": "error",
                "message": f"当前位置无法直接前往：{target}。"
            }
        else:
            agent_object.character['path'] = [(node.x, node.y) for node in path]
            agent_object.character['event'] = {
                "type": "move",
                "message": f"已移动至 `{target}` 附近。"
            }

            if target_grid_position['entryLookAt']:
                agent_object.character['look_at'] = target_grid_position['entryLookAt']
            else:
                agent_object.character['look_at'] = []
            
        waiting_time = 0.5 * len(path)                  # 计算客户端执行这个命令需要的时间，此期间服务器暂停发送指令，单位为秒。
        return {
            "waiting_time": waiting_time,
            "emit_message_type": "updateState",
            "emit_message_value": ""
        }
        
        
@register_function_call_class
class GetNews(BaseFunctionCall):
    
    def call(
        agent_object: object, 
    ):
        """刷一条新闻。

        Args:
            agent_object (object): agent 对象，通常传入 self 即可。
        """
        news: List[Dict] = NewsFetcher.fetch_news(num=1)
        agent_object.character['state'] = "reading"
        agent_object.character["event"] = {
            "type": "news",
            "contents": news
        }

        hunger_change = -0.5
        energe_change = -0.            # 暂时不做 sleep
        
        agent_object.character['current_hunger'] = max(
            0,
            agent_object.character['current_hunger'] + hunger_change, 
        )
        
        agent_object.character['current_energe'] = max(
            0,
            agent_object.character['current_energe'] + energe_change,
        )
        
        agent_object.character['hunger_change'] = hunger_change
        agent_object.character['energe_change'] = energe_change
        
        return {
            "waiting_time": 30.,
            "emit_message_type": "updateState",
            "emit_message_value": "reading"
        }


@register_function_call_class
class GetGeekNewsHotList(BaseFunctionCall):
    
    def call(
        agent_object: object, 
    ):
        """查看当前稀土掘金（一个极客、代码论坛）上有哪些热点新闻。

        Args:
            agent_object (object): agent 对象，通常传入 self 即可。
        """
        news: List[Dict] = GeekNewsFetcher.fetch_hot_list()
        agent_object.character['state'] = "reading"
        agent_object.character["event"] = {
            "type": "find_geek_news",
            "contents": news
        }
        
        hunger_change = -0.5
        energe_change = -0.            # 暂时不做 sleep
        
        agent_object.character['current_hunger'] = max(
            0,
            agent_object.character['current_hunger'] + hunger_change, 
        )
        
        agent_object.character['current_energe'] = max(
            0,
            agent_object.character['current_energe'] + energe_change,
        )
        
        agent_object.character['hunger_change'] = hunger_change
        agent_object.character['energe_change'] = energe_change
        
        return {
            "waiting_time": 30.,
            "emit_message_type": "updateState",
            "emit_message_value": ""
        }
        

@register_function_call_class
class ChooseOneGeekNews(BaseFunctionCall):
    
    def call(
        agent_object: object, 
        article_id: str
    ):
        """在稀土掘金的热点新闻目录中选择一条感兴趣的新闻查看具体内容。

        Args:
            agent_object (object): agent 对象，通常传入 self 即可。
            article_id (str): 新闻 id。
        """
        news_info_dict = GeekNewsFetcher.fetch_geek_news(article_id=article_id)
        agent_object.character['state'] = "reading"
        agent_object.character["event"] = {
            "type": "read_geek_news",
            "content": news_info_dict
        }
        
        hunger_change = -0.5
        energe_change = -0.            # 暂时不考虑 sleep
        
        agent_object.character['current_hunger'] = max(
            0,
            agent_object.character['current_hunger'] + hunger_change, 
        )
        
        agent_object.character['current_energe'] = max(
            0,
            agent_object.character['current_energe'] + energe_change,
        )
        
        agent_object.character['hunger_change'] = hunger_change
        agent_object.character['energe_change'] = energe_change
        
        return {
            "waiting_time": 60.,
            "emit_message_type": "updateState",
            "emit_message_value": ""
        }
    
    def validate_func(
        agent_object: object,
        room: dict
    ):
        return agent_object.character['event'].get('type', '') == "find_geek_news"


@register_function_call_class
class GetLeetCodeList(BaseFunctionCall):
    
    def call(
        agent_object: object, 
    ):
        """获取 LeetCode 上的题目列表，准备刷题（必须先走到「电脑桌」旁才允许选择此函数）。

        Args:
            agent_object (object): agent 对象，通常传入 self 即可。
        """
        questions = LeetCodeFetcher.get_leetcode_hot_list()
        agent_object.character['state'] = "coding"
        agent_object.character["event"] = {
            "type": "find_leetcode_list",
            "questions": questions
        }
        
        hunger_change = -0.2
        energe_change = -0.            # 暂时不做 sleep
        
        agent_object.character['current_hunger'] = max(
            0,
            agent_object.character['current_hunger'] + hunger_change, 
        )
        
        agent_object.character['current_energe'] = max(
            0,
            agent_object.character['current_energe'] + energe_change,
        )
        
        agent_object.character['hunger_change'] = hunger_change
        agent_object.character['energe_change'] = energe_change
        
        return {
            "waiting_time": 10.,
            "emit_message_type": "updateState",
            "emit_message_value": ""
        }


@register_function_call_class
class ChooseOneLeetCodeQuestion(BaseFunctionCall):
    
    def call(
        agent_object: object, 
        titleSlug: str
    ):
        """从 LeetCode 题目列表中选择一道进行刷题。

        Args:
            agent_object (object): agent 对象，通常传入 self 即可。
            titleSlug (str): 题目名称。
        """
        question_details = LeetCodeFetcher.get_question_details(titleSlug)
        
        # call api to get code result
        prompt = "根据下面的LeetCode题目描述和给出的模板，不允许额外使用 from xxx import xxx 的方式解题。写出对应的 python 代码，只写出代码即可，不要有多余的话。\n\n题目：{question}\n代码格式：{code_template}".format(
            question=re.sub(r'<[^>]+>', '', question_details['translatedContent']),
            code_template=question_details['code_template']
        )
        
        code_str = LLMClient.get_response_by_api(
            prompt=prompt
        )
        
        code_str = code_str.replace('```python', '').replace('```', '').strip()
        code_res = LeetCodeFetcher.run_code_and_get_result(
            question_id=question_details['questionId'],
            code=code_str,
            test_data=question_details['test_case']
        )
        
        agent_object.character['state'] = "coding"
        agent_object.character["event"] = {
            "type": "complete_leetcode_question",
            "question_details": question_details,
            "code_result": code_res,
            "code": code_str
        }
        
        hunger_change = -1.0
        energe_change = -0.            # 暂时不做 sleep
        
        agent_object.character['current_hunger'] = max(
            0,
            agent_object.character['current_hunger'] + hunger_change, 
        )
        
        agent_object.character['current_energe'] = max(
            0,
            agent_object.character['current_energe'] + energe_change,
        )
        
        agent_object.character['hunger_change'] = hunger_change
        agent_object.character['energe_change'] = energe_change
        
        return {
            "waiting_time": 60.,
            "emit_message_type": "updateState",
            "emit_message_value": ""
        }
    
    def validate_func(
        agent_object: object,
        room: dict
    ):
        return agent_object.character['event'].get('type', '') == "find_leetcode_list"
    

@register_function_call_class
class GetBooks(BaseFunctionCall):
    
    def call(
        agent_object: object, 
    ):
        """读一本书。

        Args:
            agent_object (object): agent 对象，通常传入 self 即可。
        """
        book_content = BooksFetcher.fetch_book_contents(
            paragrah_num=1
        )
        agent_object.character['state'] = "reading"
        agent_object.character["event"] = {
            "type": "book",
            "book_name": book_content['book_name'],
            "paragraphs": book_content['paragraphs']
        }
        
        hunger_change = -0.5
        energe_change = -0.            # 暂时不做 sleep
        
        agent_object.character['current_hunger'] = max(
            0,
            agent_object.character['current_hunger'] + hunger_change, 
        )
        
        agent_object.character['current_energe'] = max(
            0,
            agent_object.character['current_energe'] + energe_change,
        )
        
        agent_object.character['hunger_change'] = hunger_change
        agent_object.character['energe_change'] = energe_change
        
        return {
            "waiting_time": 30.,
            "emit_message_type": "updateState",
            "emit_message_value": ""
        }
        

@register_function_call_class
class Search(BaseFunctionCall):
    
    def call(
        agent_object: object, 
        query: str
    ):
        """使用搜索工具来获取想要知道的信息。

        Args:
            agent_object (object): agent 对象，通常传入 self 即可。
            query (str): 搜索关键词。
        """
        search_results = SearchFetcher.fetch_search_results(query)
        agent_object.character['state'] = "searching"
        agent_object.character["event"] = {
            "type": "search",
            "query": query,
            "results": search_results
        }
        
        hunger_change = -0.5
        energe_change = -0.            # 暂时不做 sleep
        
        agent_object.character['current_hunger'] = max(
            0,
            agent_object.character['current_hunger'] + hunger_change, 
        )
        
        agent_object.character['current_energe'] = max(
            0,
            agent_object.character['current_energe'] + energe_change,
        )
        
        agent_object.character['hunger_change'] = hunger_change
        agent_object.character['energe_change'] = energe_change
        
        return {
            "waiting_time": 60.,
            "emit_message_type": "updateState",
            "emit_message_value": ""
        }
    

@register_function_call_class
class AddMemory(BaseFunctionCall):
    
    def call(
        agent_object: object, 
        memory_content: str
    ):
        """添加一条记忆信息，通常发生在获取了新的信息之后。

        Args:
            agent_object (object): agent 对象，通常传入 self 即可。
            memory_content (str): 需要添加的记忆内容，一条概括性的关键信息。
        """
        agent_object.character['memories'].append(memory_content)
        agent_object.character['memories']  = agent_object.character['memories'][-agent_object.character['max_memory']:]      # 只保留最近的记忆
        agent_object.character['event'] = {
            'type': 'add_memory',
            'result': 'success'
        }
        
        return {
            "waiting_time": 1.,
            "emit_message_type": "updateState",
            "emit_message_value": ""
        }


@register_function_call_class
class ChangePersonality(BaseFunctionCall):
    
    def call(
        agent_object: object, 
        personality_content: str
    ):
        """修改当前人设，当获取了足够多的记忆信息，出现了新的认知后，通过该函数改变自身人设。

        Args:
            agent_object (object): agent 对象，通常传入 self 即可。
            memory_content (str): 
        """
        agent_object.character['personality'] = personality_content
        agent_object.character['event'] = {
            'type': 'change_personality',
            'result': 'success'
        }
        
        return {
            "waiting_time": 1.,
            "emit_message_type": "updateState",
            "emit_message_value": ""
        }
        
        
@register_function_call_class
class Cooking(BaseFunctionCall):
    
    def call(
        agent_object: object,
        food_name: str
    ):
        """根据当前的饱食度判断是否调用，决定是否开始做饭并进食以回复饱食度。

        Args:
            agent_object (object): agent 对象，通常传入 self 即可。
            food_name (str): 想要做的菜名，根据当前的饱腹情况来自主决定要做什么菜。
        """
        agent_object.character['state'] = "cooking"
        agent_object.character['event'] = {
            "type": "cook",
            "message": food_name
        }
        
        hunger_change = 20
        
        agent_object.character['current_hunger'] = min(
            100,
            agent_object.character['current_hunger'] + hunger_change
        )
        
        agent_object.character['hunger_change'] = hunger_change
        
        return {
            "waiting_time": 30.,
            "emit_message_type": "updateState",
            "emit_message_value": ""
        }
        
    def validate_func(
        agent_object: object,
        room: dict
    ):
        item_position = get_item_position(
            room['items'], 
            "厨房_燃气灶"
        )
        position = item_position['entryGridPosition'] if item_position['entryGridPosition'] \
                    else item_position['gridPosition']
        
        return distance(
            agent_object.character['position'],
            position
        ) <= 2
        
        
@register_function_call_class
class PostWeibo(BaseFunctionCall):
    
    def call(
        agent_object: object,
        weibo_content: str
    ):
        """当遇到有趣的事情想跟朋友们分享，或者想抒发自己观点的时候调用该函数来发布一条新的微博。

        Args:
            agent_object (object): agent 对象，通常传入 self 即可。
            weibo_content (str): 待发布的微博内容。
        """
        weibo_url = WeiBoTools.post_weibo(
            weibo_content
        )
        
        # weibo_url = "https://m.weibo.cn/u/7962675853?"
        
        agent_object.character['state'] = "posting"
        agent_object.character['event'] = {
            "type": "post_weibo",
            "content": weibo_content,
            "weibo_url": weibo_url
        }
        
        hunger_change = -0.5
        energe_change = -0.            # 暂时不做 sleep
        
        agent_object.character['current_hunger'] = max(
            0,
            agent_object.character['current_hunger'] + hunger_change, 
        )
        
        agent_object.character['current_energe'] = max(
            0,
            agent_object.character['current_energe'] + energe_change,
        )
        
        agent_object.character['hunger_change'] = hunger_change
        agent_object.character['energe_change'] = energe_change
        
        return {
            "waiting_time": 10.,
            "emit_message_type": "updateState",
            "emit_message_value": ""
        }
        
    def validate_func(
        agent_object: object,
        room: dict
    ):
        if (
            not WeiBoTools.LAST_POST_TIME
            or
            time.time() - WeiBoTools.LAST_POST_TIME > 60 * 60           # 1h 内只能发一次
        ):
            return True
        else:
            return False
        
        
@register_function_call_class
class CheckWeiBoComments(BaseFunctionCall):
    
    def call(
        agent_object: object
    ):
        """查看自己发布的最新微博现在是否有新的评论。

        Args:
            agent_object (object): agent 对象，通常传入 self 即可。
        """
        def parse_mid(analysis_extra: str):
            parts = analysis_extra.split('|')
            mid_value = None
            for part in parts:
                if part.startswith('mid:'):
                    mid_value = part.split(':')[1]
                    break
            return mid_value
        
        all_weibo = WeiBoTools.get_all_my_post_weibo()
        
        if not all_weibo:
            agent_object.character['event'] = {
                "type": "error",
                "message": "未找到任何微博。"
            }
            return {"waiting_time": 10.0}
        else:
            newest_weibo = all_weibo[0]

            weibo_info = {
                "id": newest_weibo['id'],
                "content": newest_weibo['text_raw'],
                "region_name": newest_weibo['region_name'],
                "source": newest_weibo['source'],
                "created_at": WeiBoTools.convert_weibo_datetime(newest_weibo['created_at']),
            }
            
            comments = WeiBoTools.get_all_comments(
                newest_weibo['id']
            )
            
            comments = [
                {
                    "id": comment['rootidstr'],                                        # 若回复该评论，需要该字段
                    "mid": parse_mid(comment['analysis_extra']),                # 若回复该评论，需要该字段
                    "user_name": comment["user"]["screen_name"],
                    "description": comment["user"]["description"],
                    "content": comment['text_raw'],
                    "created_at": WeiBoTools.convert_weibo_datetime(comment['created_at']),
                    
                } for comment in comments
            ]
            
            agent_object.character['state'] = "checking"
            agent_object.character['event'] = {
                "type": "check_weibo_comments",
                "weibo_info": weibo_info,
                "comments": comments
            }
            
            return {
                "waiting_time": 30.,
                "emit_message_type": "updateState",
                "emit_message_value": ""
            }
            

@register_function_call_class
class ReplyWeiboComment(BaseFunctionCall):
    
    def call(
        agent_object: object,
        id: str,
        mid: str,
        user_name: str,
        content: str,
        reply_content: str
    ):
        """回复一条网友的微博评论。

        Args:
            agent_object (object): agent 对象，通常传入 self 即可。
            id (str): comment dict 中的 id 字段。
            mid (str): comment dict 中的 mid 字段。
            user_name (str): 评论者的用户名。
            content (str): 评论者的评论内容。
            reply_content (str): 回复的内容。

        Returns:
            _type_: _description_
        """
        reply_result = WeiBoTools.reply_comment(
            cid=id,
            mid=mid,
            reply_content=reply_content
        )
        
        # reply_result = True
        
        agent_object.character['state'] = "replying"
        agent_object.character['event'] = {
            "type": "reply_weibo_comment",
            "reply_content": reply_content if reply_result else "回复失败",
            "user_name": user_name,
            "comment_content": content
        }
        
        return {
            "waiting_time": 10.0,
            "emit_message_type": "updateState",
            "emit_message_value": ""
        }
        
    def validate_func(
        agent_object: object,
        room: dict
    ):
        return agent_object.character['event'].get('type', '') == "check_weibo_comments"
        

def generate_all_function_calls_prompts() -> str:
    """
    为所有已经注册的函数，生成调用 prompt。
    """
    prompt = "当前所有可使用的函数以及对应的解释如下：\n\n"
    
    for function_name, function_value in ALL_FUNCTIONS.items():
        prompt += f"* {function_name}: {function_value['docstring']}\n"
    
    # prompt += '\n现在请你选择一个函数执行，只用生成python调用代码即可，不要有多余的话。'
    return prompt


def generate_valid_function_calls_prompts(
    agent_object: object,
    room: dict
) -> str:
    """找到当前状态下所有可用的函数，生成调用 prompt。

    Args:
        agent_object (object): _description_
        items (list): _description_
        room (dict): _description_
    """
    prompt = "当前所有可使用的函数以及对应的解释如下：\n\n"
    
    for function_name, function_value in ALL_FUNCTIONS.items():
        if function_value['validate_func'](agent_object, room):
            prompt += f"* {function_name}: {function_value['docstring']}\n"
    
    return prompt    


if __name__ == "__main__":
    # print(ALL_FUNCTIONS)
    # print(eval(list(ALL_FUNCTIONS.keys())[1]))
    print(generate_all_function_calls_prompts())
        