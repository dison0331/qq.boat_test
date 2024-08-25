# -*- coding: utf-8 -*-
import os
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


@Commands("/帮助")
async def help_list(api: BotAPI, message: Message, params=None):
    _log.info("发送帮助文档")
    message_reference = Reference(message_id=message.id)
    await api.post_message(
        channel_id=message.channel_id,
        content=help_list,
        msg_id=message.id,
        message_reference=message_reference,
    )
    return True


class MyClient(botpy.Client):
    async def on_at_message_create(self, message: Message):
        # 注册指令handler
        handlers = [
            help_list
        ]
        for handler in handlers:
            if await handler(api=self.api, message=message):
                return


if __name__ == "__main__":
    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_guild_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=config["appid"], secret=config["secret"])