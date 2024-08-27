# -*- coding: utf-8 -*-
import os
import time
import yaml
import botpy
from botpy import logging, BotAPI
from botpy.ext.command_util import Commands
from botpy.message import Message
from botpy.ext.cog_yaml import read
from botpy.types.message import Reference


def load_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    return data


config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))
text = load_yaml('text.yaml')
help_list = text["help_list"]

child_stiitings_error = text["child_stiitings_error"]
_log = logging.get_logger()


@Commands("帮助")
async def help_h(api: BotAPI, message: Message, params=None):
    _log.info("发送帮助文档")
    message_reference = Reference(message_id=message.id)
    await api.post_message(
        channel_id=message.channel_id,
        content=help_list,
        msg_id=message.id,
        message_reference=message_reference,
    )
    return True


@Commands("报时")
async def baoshi(api: BotAPI, message: Message, params=None):
    t = time.strftime("%Y-%m-%d, %H:%M:%S")
    _log.info(f"报送现在的时间（服务器）'{t}'")
    message_reference = Reference(message_id=message.id)
    await api.post_message(
        channel_id=message.channel_id,
        content='编号为 ' + message.author.id + f''' 的用户你好现在的时间是 “{t} ” 
     注意：
（attention）：
                  时间可能存有一定延迟，仅供参考！
    （Time may have some delay error, for reference only.）''',

        msg_id=message.id,
        message_reference=message_reference,
    )
    return True


@Commands("问好")
async def wenhao(api: BotAPI, message: Message, params=None):
    t = time.strftime("%Y-%m-%d, %H:%M:%S")
    _log.info(f"发送问好语句（时间为{t}）")
    message_reference = Reference(message_id=message.id)
    await api.post_message(
        channel_id=message.channel_id,
        content=f'''现在是“{t}”。你好，很高兴认识你!
    Now is '{t}'.Hi,nice to meet you!''',

        msg_id=message.id,
        message_reference=message_reference,
    )
    return True


@Commands("举报")
async def jvbao(api: BotAPI, message: Message, params=None):
    t = time.strftime("%Y-%m-%d, %H:%M:%S")
    _log.info(f"{t}收到举报！")
    message_reference = Reference(message_id=message.id)
    await api.post_message(
        channel_id=message.channel_id,
        content=message.author.id + ''' 号用户你好，收到并记录你的举报了，管理员正在赶来''',
        msg_id=message.id,
        message_reference=message_reference,
    )
    return True


@Commands("获取属于我的ID")
async def get_id(api: BotAPI, message: Message, params=None):
    t = time.strftime("%Y-%m-%d, %H:%M:%S")
    _log.info(f"{t}有用户获取ID")
    message_reference = Reference(message_id=message.id)
    await api.post_message(
        channel_id=message.channel_id,
        content='用户你好，你的id是 ' + message.author.id,
        msg_id=message.id,
        message_reference=message_reference,
    )
    return True


@Commands("禁言")
async def mute(api: BotAPI, message: Message, params=None):
    _log.info("执行禁言操作")

    # 确保 message.mentions 至少有一个用户
    if message.mentions and len(message.mentions) > 1:
        user = message.mentions[1]  # 获取第一个提到的用户

        # 从消息内容中解析禁言时间
        try:
            # 假设格式为: @机器人 /禁言 @禁言者 时间
            parts = message.content.split()
            mute_seconds = int(parts[-1])  # 假设时间是最后一个部分
        except (IndexError, ValueError):
            _log.warning("无法解析禁言时间，默认禁言20秒")
            mute_seconds = 20  # 设置默认禁言时间

        # 检查是否试图禁言自己
        if user.id == message.author.id:
            await api.post_message(
                channel_id=message.channel_id,
                content="你不能禁言自己！",
                msg_id=message.id
            )
            _log.info("用户试图禁言自己，操作已阻止")
            return False

        message_reference = Reference(message_id=message.id)

        # 正确获取用户的用户名，并显示禁言时间
        await api.post_message(
            channel_id=message.channel_id,
            content=f"{user.username} 被禁言 {mute_seconds} 秒",
            msg_id=message.id,
            message_reference=message_reference,
        )

        # 禁言成员
        await api.mute_member(
            guild_id=message.guild_id,
            user_id=user.id,
            mute_seconds=mute_seconds
        )
    else:
        _log.warning("没有提到的用户，无法执行禁言操作")
        await api.post_message(
            channel_id=message.channel_id,
            content="请提到要禁言的用户。",
            msg_id=message.id
        )

    return True


class MyClient(botpy.Client):
    async def on_at_message_create(self, message: Message):
        # 注册指令handler
        handlers = [
            help_h,
            baoshi,
            wenhao,
            jvbao,
            get_id,
            mute
        ]
        for handler in handlers:
            if await handler(api=self.api, message=message):
                return


if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_guild_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_guild_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=config["appid"], secret=config["secret"])
