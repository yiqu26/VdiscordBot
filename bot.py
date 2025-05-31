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

        # Bilibili 影片
        elif "bilibili.com/video/" in message.content:
            for word in message.content.split():
                if "bilibili.com/video/" in word:
                    clean_url = word.split("?")[0]
                    converted_url = clean_url.replace("https://www.bilibili.com", "https://www.vxbilibili.com")\
                                             .replace("http://www.bilibili.com", "https://www.vxbilibili.com")\
                                             .replace("https://bilibili.com", "https://www.vxbilibili.com")\
                                             .replace("http://bilibili.com", "https://www.vxbilibili.com")
                    content = f"🎬 **由 @{sender} 提供的 Bilibili 影片：**\n👉 {converted_url}"
                    await self.send_with_webhook(message, content)
                    break

        # Bilibili 短連結
        elif "b23.tv/" in message.content:
            for word in message.content.split():
                if "b23.tv/" in word:
                    clean_url = word.split("?")[0]
                    converted_url = clean_url.replace("https://b23.tv", "https://vxb23.tv")\
                                             .replace("http://b23.tv", "https://vxb23.tv")
                    content = f"🎬 **由 @{sender} 提供的 Bilibili 短連結影片：**\n👉 {converted_url}\n⚠️ *如僅播放前段請點開觀看全片*"
                    await self.send_with_webhook(message, content)
                    break

client = AutoMediaBot()
client.run(TOKEN)
