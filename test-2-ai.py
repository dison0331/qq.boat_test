# -*- coding: utf-8 -*-
import os
import botpy
from botpy.message import Message

# 假设配置文件已经正确设置，并且包含了appid和token
# 这里我们直接跳过读取配置文件的步骤，直接定义它们
test_config = {
    "appid": "102268340",
    "token": "quy26AEINSXchmrw28EKQWcjqx4BIPXf"
}


async def handle_hi_message(message: Message):
    # 检查消息内容是否以"/hi"开头
    if message.content.startswith("/hi"):
        # 提取"/hi"之后的内容（如果有的话）
        content_after_hi = message.content[4:].strip()
        if content_after_hi:
            # 如果有内容，则回复它
            await message.reply(f"Hi there! You said: {content_after_hi}")
        else:
            # 如果没有内容，则简单回复
            await message.reply("Hi there! What's up?")


class MyClient(botpy.Client):
    async def on_at_message_create(self, message: Message):
        # 当机器人被“@”时，检查消息内容
        await handle_hi_message(message)


if __name__ == "__main__":
    # 设置事件通道的监听意图
    intents = botpy.Intents(public_guild_messages=True)
    client = MyClient(intents=intents)
    # 运行机器人，传入appid和token
    client.run(appid=test_config["appid"], token=test_config["token"])
