import discord
import os
import asyncio
import aiohttp

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

    async def expand_url(self, url):
        # 嘗試展開短網址
        try:
            async with aiohttp.ClientSession() as session:
                async with session.head(url, allow_redirects=True) as resp:
                    return str(resp.url)
        except:
            return url

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        content = message.content
        original_content = content
        urls = content.split()

        for word in urls:
            url = word.split("?")[0]

            # 展開短網址（b23.tv 或 IG share 短連結）
            if "b23.tv/" in url or ("instagram.com" in url and "?" in word):
                url = await self.expand_url(word)

            if "instagram.com/reel/" in url:
                converted = url.replace("https://www.instagram.com", "https://www.ddinstagram.com")\
                               .replace("http://www.instagram.com", "https://www.ddinstagram.com")\
                               .replace("https://instagram.com", "https://ddinstagram.com")\
                               .replace("http://instagram.com", "https://ddinstagram.com")
                await message.channel.send(f"🎬 IG Reels 轉換連結：\n👉 {converted}")
                return

            elif "instagram.com/p/" in url:
                converted = url.replace("https://www.instagram.com", "https://www.ddinstagram.com")\
                               .replace("http://www.instagram.com", "https://www.ddinstagram.com")\
                               .replace("https://instagram.com", "https://ddinstagram.com")\
                               .replace("http://instagram.com", "https://ddinstagram.com")
                await message.channel.send(f"🖼️ IG 貼文轉換連結：\n👉 {converted}")
                return

            elif "bilibili.com/video/" in url:
                converted = url.replace("https://www.bilibili.com", "https://www.vxbilibili.com")\
                               .replace("http://www.bilibili.com", "https://www.vxbilibili.com")\
                               .replace("https://bilibili.com", "https://www.vxbilibili.com")\
                               .replace("http://bilibili.com", "https://www.vxbilibili.com")
                await message.channel.send(f"📺 Bilibili 轉換連結：\n👉 {converted}")
                return

            elif "b23.tv/" in url:
                real_url = await self.expand_url(url)
                converted = real_url.replace("https://www.bilibili.com", "https://www.vxbilibili.com")\
                                    .replace("http://www.bilibili.com", "https://www.vxbilibili.com")\
                                    .replace("https://bilibili.com", "https://www.vxbilibili.com")\
                                    .replace("http://bilibili.com", "https://www.vxbilibili.com")
                await message.channel.send(f"📺 Bilibili 短連結轉換：\n👉 {converted}")
                return

client = AutoMediaBot()
client.run(TOKEN)
