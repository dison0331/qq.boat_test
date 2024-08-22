# -*- coding: utf-8 -*-
# 这是一个简单的示例，不是开发程序主体！
import os
import botpy
from botpy import logging
from botpy.ext.command_util import Commands
from botpy.message import Message
from botpy.ext.cog_yaml import read

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))
_log = logging.get_logger()

helplist = """使用说明

/举报 违规详情
    允许举报成员违规行为，需回复源消息（待开发）
    示例：/举报 宣传违规软件

！以下操作均需管理员权限方可执行！

/禁言 @指定成员 时长(以秒为单位)
    管理员审查后即可禁言指定成员（待开发）
    示例：/禁言 @AFK 100

/封禁 @指定成员
    直接踢出成员并拉进黑名单（待开发）
    示例：/封禁 @AFK 

/解封 @指定成员
    解除成员禁言状态（待开发）
    示例：/解封 @AFK

帮助文档版本：0.01beta"""


@Commands("/帮助")
async def help_list(message: Message, params=None):
    await message.reply(
        content=helplist
    )
    return True


class MyClient(botpy.Client):
    async def on_at_message_create(self, message: Message):
        # 注册指令handler
        tasks = [
            help_list
        ]
        for handler in tasks:
            if await handler(api=self.api, message=message):
                return


if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_guild_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_guild_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], token=test_config["token"])
