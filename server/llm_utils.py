import json
import random

import requests
from openai import OpenAI


model_name = "gemini-1.5-flash"                             # gemini model; 更多参考：https://ai.google.dev/gemini-api/docs/models/gemini-v2?hl=zh-cn
api_key = ""                                                    # Gemini API Key
url = "https://generativelanguage.googleapis.com/v1beta/"
# model_name = "qwen2.5-72b-instruct"                             # qwen-plus, 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
# url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
# api_key = ""                                                    # 阿里云 API Key


class LLMClient(object):
        
    @staticmethod
    def get_response_by_api(
        prompt: str,   
    ) -> str:
        messages = [
            {"role": "system", "content": "You are Gemini, created by Google. You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
        client = OpenAI(
            api_key=api_key,
            base_url=url,
        )
        completion = client.chat.completions.create(
            model=model_name,
            messages=messages,
            )

        response = json.loads(completion.model_dump_json())
        res = None
        resposne = response.get("choices", [])
        if response:
            res = resposne[0]["message"]["content"]
        
        return res

    @staticmethod
    def get_mock_response(
        prompt: str,   
    ) -> str:
        return 'goto(self, "bedDouble")'
    
    @staticmethod
    def walk_to_random_item(
        items: list,
    ) -> str:
        item = random.choice(items)
        return f'goto(self, "{item}")'
    

if __name__ == "__main__":
    res = LLMClient.get_response_by_api("你好")
    print(res)
