"""
Agent class.
"""
import json
import random
import logging
import datetime
import traceback
from logging.handlers import TimedRotatingFileHandler

from utils import find_path, distance
from llm_utils import LLMClient
from prompts.agent import BASIC_DECISION_PROMPT
from function_calls import *                            # import all function calls


class Agent(object):
    
    def __init__(
        self,
        world: object,
        room: dict,
        character: dict,
        sio: object,
        *args,
        **kwargs
    ):
        """
        Init func.

        Args:
            world (object): 世界信息，包含了其他 agent 对象。
            room (dict): 房间信息。
            character (dict): 角色信息, e.g. -> {
                                                "id": 2,
                                                "session": 2,
                                                "name": "娜",
                                                "gender": "female",
                                                "avatarName": "designer",
                                                "position": [15, 4],
                                                "path": [],
                                                "job": "产品设计",
                                                "hobby": ["做饭", "追剧"],
                                                "personality": "内向，比较害羞，酷爱追剧，认为世界是属于独立的人的，不喜欢被打扰。",
                                                "memories": [],
                                                "state": ""
                                            }
            sio (object): socket io 对象。
        """
        self.world = world
        self.room = room
        self.character = character
        self.sio = sio
        self.action_history = []
        self.max_action_history = 50
        self.interupted_flag = False            # 是否立即响应新的事件（通常用于处理外界的中断信号，比如收到来自别的角色的消息）
        self.logger = self.init_logger()
    
    def init_logger(self):
        """
        设置 logger。
        """
        logging.basicConfig(filemode='w')
        
        logger = logging.getLogger(self.character["name"])
        logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        file_handler = TimedRotatingFileHandler(
            f'logs/{self.character["name"]}.log',
            when='midnight',                        # 在午夜时分割文件
            interval=1,                             # 每1天分割一次
            backupCount=30,                         # 保留最近30天的日志
            encoding='utf-8'
        )
        file_handler.suffix = '%Y-%m-%d.log'  # 分割后的文件名后缀格式
        file_handler.setFormatter(formatter)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
        
    def random_walk(self):
        """
        在房间内随机走。
        """
        random_target_x = random.choice(range(self.room['size'][0]))
        random_target_y = random.choice(range(self.room['size'][1]))
        
        path, _ = find_path(
            self.room,
            self.character['position'],
            (random_target_x, random_target_y)
        )
        
        self.character['path'] = [(node.x, node.y) for node in path]
        self.character['event'] = {
            "type": "move",
            "message": f"已移动。"
        }
        waiting_time = 0.5 * len(path)
        return waiting_time
    
    def stay(self):
        """
        stand still.
        """
        return {"waiting_time": 5.}
    
    def random_walk_task(self):
        """
        简单测试随机游走任务。
        """
        waiting_time = self.random_walk()
        
        self.sio.emit(
            "updateState", 
            {
                "character": self.character,
                "message_value": "",
                "on_watch_num": len(self.world.connected_users)
            },
            room=1
        )
        
        self.sio.sleep(waiting_time)
        if self.character['path']:
            self.character['position'] = self.character['path'][-1]
        
        self.character['path'] = []
        self.logger.info(f"Player {self.character['id']} moved, sleep {waiting_time} seconds.")
        
    def get_current_observation(self):
        """
        根据当前事件，处理成对应的当前观测信息。
        """
        if self.character["event"]:
            if self.character["event"]['type'] == "book":
                return "你正在读一本名叫《{book_name}》的书，书中的内容是：{content}".format(
                    book_name=self.character["event"]['book_name'],
                    content=self.character["event"]['paragraphs'][0]
                )
            
            elif self.character["event"]['type'] == "news":
                return "你正在看一条新闻，新闻标题是：{title}，内容是：{content}".format(
                    title=self.character["event"]['contents'][0].get('title', ''),
                    content=self.character["event"]['contents'][0].get('content', '')[:1024]
                )
                
            elif self.character['event']['type'] == "find_geek_news":
                return f"你查找了一些极客新闻：{self.character['event']['contents']}。" 
            
            elif self.character['event']['type'] == "read_geek_news":
                content = self.character['event']['content']['content']
                if len(content) > 1024: content = content[:1024] + "..."
                return "你读了一篇技术帖，帖子名为：{title}，\n内容为：{content}".format(
                    title=self.character['event']['content']['title'],
                    content=content
                ) 
                
            elif self.character["event"]['type'] == "search":
                self.logger.info(f"{self.character['event']=}")
                return "你搜索了关于 `{query}` 的信息，结果为：{results}".format(
                    query=self.character["event"]['query'],
                    results='\n\n'.join([
                        f'标题：{r["title"]}\n搜索结果：{r["body"]}' 
                        for r in self.character["event"]['results']
                    ])
                )
            
            elif self.character["event"]['type'] == "move":
                return self.character["event"]['message']
                
            elif self.character["event"]['type'] == "cook":
                return f"你做了一道：{self.character['event']['message']}。"
            
            elif self.character["event"]['type'] == "post_weibo":
                return f"你发了一条微博：{self.character['event']['content']}。"
            
            elif self.character["event"]['type'] == "check_weibo_comments":
                weibo_content = self.character['event']['weibo_info']["content"]
                return f"你正在查看网友对你微博的评论。\n微博内容为：{weibo_content}\n最新评论内容有：{self.character['event']['comments']}"
            
            elif self.character["event"]['type'] == "reply_weibo_comment":
                return f"你回复了来自网友 `{self.character['event']['user_name']}` 的评论「{self.character['event']['comment_content']}`」：{self.character['event']['reply_content']}"
            
            elif self.character["event"]['type'] == "find_leetcode_list":
                return f"当前 LeetCode 题目列表如下：{self.character['event']['questions']}"
            
            elif self.character["event"]['type'] == "complete_leetcode_question":
                return f"你完成了一道 LeetCode 题目，结果是：{self.character['event']['code_result']}"
            
            elif self.character["event"]['type'] == "talk":
                return f"你对 `{self.character['event']['target']}` 说：{self.character['event']['message']}"
            
            elif self.character["event"]['type'] == "receive_message":
                return f"`{self.character['event']['from']}` 对你说：{self.character['event']['message']}"
            
            elif self.character["event"]['type'] == "refused_answer_by_other":
                return f"`{self.character['event']['from']}` 没有理你。"
            
            elif self.character["event"]['type'] == "error":
                return f"执行行为时遇到错误：{self.character['event']['message']} 请重新选择。"
            
            elif self.character["event"]['type'] == "add_memory":
                return f"新记忆已添加。"
            
            elif self.character["event"]['type'] == "change_personality":
                return f"人设已更新。"
            
            elif self.character["event"]['type'] == "find_someone":
                return f"你到达了 `{self.character['event']['target']}` 附近。"
            
            else:
                return "当前没有特殊事件发生。"    
        else:
            return "当前没有特殊事件发生。"
        
    def get_current_other_characters(self):
        """
        返回当前房间中所有除了自己之外的角色名字，以及附近范围内的角色名字。
        """
        other_characters_name = []
        other_nearby_characters_name = []
        
        for character in self.room['characters']:
            if character['id'] != self.character['id']:
                other_characters_name.append(character['name'])
                if distance(
                    self.character['position'], 
                    character['position']
                ) <= 1:
                    other_nearby_characters_name.append(character['name'])
                    
        return other_characters_name, other_nearby_characters_name
    
    def get_hunger_prompt_string(self):
        """
        通过 hunger 值生成对应的 prompt str。
        """
        base_prompt = f"{round(self.character['current_hunger'], 1)}/{self.character['max_hunger']}"
        
        current_hunger_percentage = (
            self.character['current_hunger'] / self.character['max_hunger']
        )
        
        if current_hunger_percentage > 0.8:
            return f"{base_prompt}（饱腹）"
        
        elif current_hunger_percentage > 0.6:
            return f"{base_prompt}（轻微饥饿）"
        
        elif current_hunger_percentage > 0.4:
            return f"{base_prompt}（饥饿）"
        
        else:
            return f"{base_prompt}（非常饥饿）"
        
    def get_energe_prompt_string(self):
        """
        通过 energe 值生成对应的 prompt str。
        """
        base_prompt = f"{round(self.character['current_energe'], 1)}/{self.character['max_energe']}"
        current_energe_percentage = self.character['current_energe'] / self.character['max_energe']
        
        if current_energe_percentage > 0.8:
            return f"{base_prompt}（精力充沛）"
        
        elif current_energe_percentage > 0.6:
            return f"{base_prompt}（轻微疲惫）"
        
        elif current_energe_percentage > 0.4:
            return f"{base_prompt}（疲惫）"
        
        else:
            return f"{base_prompt}（非常疲惫）"
        
    def planning(self):
        """
        self planing what to do next.
        """
        cur_personality_setting = {
            "name": self.character['name'],
            "gender": self.character['gender'],
            "job": self.character['job'],
            "hobby": self.character['hobby'],
            "personality": self.character['personality'],
        }
        
        current_items = [item['name'] for item in self.room['items']]

        action_space_prompt = generate_valid_function_calls_prompts(
            self,
            self.room
        )

        current_other_characters, current_nearby_characters = self.get_current_other_characters()
        
        CUR_PLANNING_PROMPT = BASIC_DECISION_PROMPT.format(
            current_personality_setting=cur_personality_setting,
            currrent_memory=self.character['memories'],
            currrent_action_space=action_space_prompt,
            current_items=current_items,            
            current_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
            current_other_characters=current_other_characters,
            current_nearby_characters=current_nearby_characters,
            current_observation=self.get_current_observation(),
            action_history=self.action_history,
            current_hunger=self.get_hunger_prompt_string(),
            current_energy=self.get_energe_prompt_string()
        )
        
        self.logger.info(CUR_PLANNING_PROMPT)
        # exit()
        
        llm_result = LLMClient.get_response_by_api(
            CUR_PLANNING_PROMPT
        )
        
        # if self.character['id'] == 1:
        #     self.character['position'] = [11, 10]
        #     llm_result = """{"execute": "GetBooks.call(self)", "thought": "测试"}"""
        #     # llm_result = """{"execute": "DoNothing.call(self)", "thought": "测试"}"""
        # else:
        #     llm_result = """{"execute": "DoNothing.call(self)", "thought": "测试"}"""
        
        try:
            self.logger.info(f"{llm_result=}")
            llm_result = json.loads(llm_result)
            
            func_to_call = llm_result["execute"]
            self.character['current_thought'] = llm_result["thought"]
            
            func_res = eval(func_to_call)
            self.action_history.append(func_to_call)
            self.action_history = self.action_history[-self.max_action_history:]
        except:
            self.logger.error(traceback.format_exc())
            func_res = {}
        
        return_dict = {}     
        if func_res:
            return_dict["waiting_time"] = func_res.get("waiting_time", 0.)
            return_dict["emit_message_type"] = func_res.get("emit_message_type", "")
            return_dict["emit_message_value"] = func_res.get("emit_message_value", "")
        
        return return_dict
    
    def sleep_with_interupted_check(
        self, 
        waiting_time: float,
        interval: float = 0.1
    ):
        """
        执行任务的同时，监测是否有外界中断信号，若存在中断信号，则立即响应。

        Args:
            waiting_time (float): _description_
            interval (float): 检查间隔时间（秒）
        """
        elapsed_time = 0
        while elapsed_time < waiting_time:
            if self.interupted_flag:
                self.interupted_flag = False
                break
            self.sio.sleep(interval)
            elapsed_time += interval
        
    def main_loop(self):
        """Update self state, and return."""
        
        for _ in range(3):
            self.random_walk_task()
            print(self.character['position'])
        
        while True:
            
            result = self.planning()
            
            self.logger.info(f"{result=}")
            self.logger.info(f"{self.character['event']=}")
            
            if result.get('emit_message_type', ''):
                self.sio.emit(
                    result['emit_message_type'], 
                    {
                        "character": self.character,
                        "message_value": result['emit_message_value'],
                        "on_watch_num": len(self.world.connected_users)
                    },
                    room=1
                )
            
            waiting_time = result.get("waiting_time", 0.)
            self.sleep_with_interupted_check(waiting_time)