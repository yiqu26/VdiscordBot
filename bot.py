import discord
import os
import asyncio
import aiohttp
from urllib.parse import urlparse, urlunparse

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

    def remove_query_params(self, url):
        parsed = urlparse(url)
        return urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))

    async def expand_url(self, url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.head(url, allow_redirects=True) as resp:
                    return str(resp.url)
        except:
            return url

    def convert_instagram(self, url):
        for pattern in [
            "https://www.instagram.com", "http://www.instagram.com",
            "https://instagram.com", "http://instagram.com"
        ]:
            if url.startswith(pattern):
                return url.replace(pattern, "https://www.ddinstagram.com")
        return url

    def convert_bilibili(self, url):
        for pattern in [
            "https://www.bilibili.com", "http://www.bilibili.com",
            "https://bilibili.com", "http://bilibili.com"
        ]:
            if url.startswith(pattern):
                return url.replace(pattern, "https://www.vxbilibili.com")
        return url

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        content = message.content
        sender = message.author.display_name
        urls = content.split()

        for word in urls:
            url = word.split("?")[0]

            if "b23.tv/" in url or ("instagram.com" in url and "?" in word):
                url = await self.expand_url(word)

            url = self.remove_query_params(url)

            try:
                await message.delete()
            except discord.Forbidden:
                print("⚠️ 沒有刪除訊息權限")

            if "instagram.com/reel/" in url:
                converted = self.convert_instagram(url)
                await message.channel.send(f"🎬 由 @{sender} 提供的 IG Reels：\n👉 {converted}")
                return

            elif "instagram.com/p/" in url:
                converted = self.convert_instagram(url)
                await message.channel.send(f"🖼️ 由 @{sender} 提供的 IG 貼文：\n👉 {converted}")
                return

            elif "bilibili.com/video/" in url:
                converted = self.convert_bilibili(url)
                await message.channel.send(f"📺 由 @{sender} 提供的 Bilibili 影片：\n👉 {converted}")
                return

            elif "b23.tv/" in url:
                real_url = await self.expand_url(url)
                real_url = self.remove_query_params(real_url)
                converted = self.convert_bilibili(real_url)
                await message.channel.send(f"📺 由 @{sender} 提供的 Bilibili 短連結：\n👉 {converted}")
                return

client = AutoMediaBot()
client.run(TOKEN)
