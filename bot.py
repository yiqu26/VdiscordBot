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

    async def try_fetch_url(self, session, url):
        for attempt in range(3):
            try:
                async with session.get(url, timeout=5) as r:
                    if r.status == 200:
                        return True
            except:
                pass
            await asyncio.sleep(1)
        return False

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        sender = message.author.display_name

        def simplify_url(url: str) -> str:
            return url.split("?")[0]

        async with message.channel.typing():
            # IG Reels / 貼文處理
            if "instagram.com/reel/" in message.content or "instagram.com/p/" in message.content:
                for word in message.content.split():
                    if "instagram.com/reel/" in word or "instagram.com/p/" in word:
                        clean_url = simplify_url(word)
                        proxies = ["ddinstagram.com", "g.ddinstagram.com", "d.ddinstagram.com"]
                        converted_url = None

                        async with aiohttp.ClientSession() as session:
                            for proxy in proxies:
                                candidate = clean_url.replace("https://www.instagram.com", f"https://{proxy}") \
                                                     .replace("http://www.instagram.com", f"https://{proxy}") \
                                                     .replace("https://instagram.com", f"https://{proxy}") \
                                                     .replace("http://instagram.com", f"https://{proxy}")
                                if await self.try_fetch_url(session, candidate):
                                    converted_url = candidate
                                    break

                        # 備援切換為 instagramez.com
                        if not converted_url:
                            path = clean_url.split("instagram.com")[-1]
                            converted_url = f"https://instagramez.com{path}"

                        try:
                            await message.delete()
                        except discord.Forbidden:
                            print("⚠️ 無法刪除 IG 訊息")

                        await asyncio.sleep(1.5)
                        await message.channel.send(
                            f"🎬 由 @{sender} 提供的 IG Reels：\n👉 {converted_url}"
                        )
                        break
