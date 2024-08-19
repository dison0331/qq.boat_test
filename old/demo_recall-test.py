# -*- coding: utf-8 -*-
#这是一个简单的示例，不是开发程序主体！
import requests
import os
import botpy
from botpy import logging
from botpy.message import Message
from botpy.ext.cog_yaml import read

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))
_log = logging.get_logger()

class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_at_message_create(self, message: Message):
        if message.content.startswith("@"):
            # 获取@后面的内容
            question = message.content[1:].strip()
            # 返回相应的回答
            answer = "对不起，我不明白你的问题。请重新表述你的问题。"

        if question == "天气如何？":
            
           def get_weather():
               api_key = "YOUR_API_KEY"  # Seniverse API密钥
               city = "北京"  # 替换为您想要查询天气的城市名称
               url = f"https://api.seniverse.com/v3/weather/daily.json?city={city}&key={api_key}"
               response = requests.get(url)
               data = response.json()
               weather_info = data["results"][0]["forecasts"][0]["desc"]  # 获取天气描述信息
           return weather_info

                 # 调用函数并打印天气信息
             weather = get_weather()

            _message = await message.reply("今天的天气是int(wpreather)")  # 根据实际情况提供天气信息


        
        elif question == "有什么新闻？":
           import newsapi

def get_news_summary():
    # 创建一个新闻API的客户端
    news_client = newsapi.NewsClient()
    
    # 获取今日的新闻摘要
    today_summary = news_client.get_top_headlines()
    
    # 返回新闻摘要
    return today_summary

# 在elif语句中使用get_news_summary函数
elif question == "有什么新闻？":
    news_summary = get_news_summary()
    print(news_summary)
        else:
            _message = await message.reply("对不起，我不明白你的问题。")

        await self.api.recall_message(message.channel_id, _message.get("id"), hidetip=True)
