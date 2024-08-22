import botpy
from botpy.types.message import Message


class SimpleBot(botpy.Client):
    async def on_at_message_create(self, message: Message):
        # 当机器人被@时，回复一条消息
        await self.api.post_message(
            channel_id=message.channel_id,
            content=f"Hello, {message.author.username}! I'm SimpleBot."
        )

    # 设置Intents，这里我们只需要监听公域消息


intents = botpy.Intents(public_guild_messages=True)

# 创建并运行机器人客户端
# 注意：你需要替换{appid}和{token}为你的实际App ID和Token
client = SimpleBot(intents=intents)
client.run(appid='{102268340}', token='{rVfAQSNq5E8PWjyfhoZms2JkKrC85mRE}')
