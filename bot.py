import discord
import os
import asyncio

TOKEN = os.getenv("TOKEN")

class AutoMediaBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)

    async def on_ready(self):
        print(f"✅ Bot 上線：{self.user}")
        try:
            await self.tree.sync()
        except Exception as e:
            print(f"❌ 指令同步失敗：{e}")

    async def send_with_webhook(self, message, content):
        try:
            webhook = await message.channel.create_webhook(name="MediaPreviewBot")
            await webhook.send(
                content=content,
                username=message.author.display_name,
                avatar_url=message.author.avatar.url if message.author.avatar else None
            )
            await webhook.delete()
            await message.delete()
        except discord.Forbidden:
            await message.channel.send(content)

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        sender = message.author.display_name

        # IG Reels
        if "instagram.com/reel/" in message.content:
            for word in message.content.split():
                if "instagram.com/reel/" in word:
                    clean_url = word.split("?")[0]
                    converted_url = clean_url.replace("https://www.instagram.com", "https://www.ddinstagram.com")\
                                             .replace("http://www.instagram.com", "https://www.ddinstagram.com")\
                                             .replace("https://instagram.com", "https://ddinstagram.com")\
                                             .replace("http://instagram.com", "https://ddinstagram.com")
                    content = f"🎬 **由 @{sender} 提供的 IG Reels：**\n👉 {converted_url}"
                    await self.send_with_webhook(message, content)
                    break

        # IG 貼文 post
        elif "instagram.com/p/" in message.content:
            for word in message.content.split():
                if "instagram.com/p/" in word:
                    clean_url = word.split("?")[0]
                    converted_url = clean_url.replace("https://www.instagram.com", "https://www.ddinstagram.com")\
                                             .replace("http://www.instagram.com", "https://www.ddinstagram.com")\
                                             .replace("https://instagram.com", "https://ddinstagram.com")\
                                             .replace("http://instagram.com", "https://ddinstagram.com")
                    content = f"🖼️ **由 @{sender} 提供的 IG 貼文：**\n👉 {converted_url}"
                    await self.send_with_webhook(message, content)
                    break

client = AutoMediaBot()
client.run(TOKEN)
