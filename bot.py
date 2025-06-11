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
            # IG Reels / 貼文
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

                        if not converted_url:
                            path = clean_url.split("instagram.com")[-1]
                            converted_url = f"https://instagramez.com{path}"

                        try:
                            await message.delete()
                        except discord.Forbidden:
                            print("⚠️ 無法刪除 IG 訊息")

                        await asyncio.sleep(1.5)
                        await message.channel.send(
                            f"🎮 由 @{sender} 提供的 IG Reels：\n👉 {converted_url}"
                        )
                        break

            # Bilibili 短/長連結
            elif "bilibili.com/video/" in message.content or "b23.tv/" in message.content:
                for word in message.content.split():
                    if "bilibili.com/video/" in word or "b23.tv/" in word:
                        clean_url = simplify_url(word)

                        if "b23.tv/" in clean_url:
                            try:
                                timeout = aiohttp.ClientTimeout(total=5)
                                async with aiohttp.ClientSession(timeout=timeout) as session:
                                    async with session.head(clean_url, allow_redirects=True) as resp:
                                        resolved_url = str(resp.url)
                                        clean_url = simplify_url(resolved_url)
                            except Exception as e:
                                print(f"⚠️ 短連結解析失敗：{e}")

                        converted_url = clean_url.replace("https://www.bilibili.com", "https://www.vxbilibili.com") \
                                                 .replace("http://www.bilibili.com", "https://www.vxbilibili.com") \
                                                 .replace("https://bilibili.com", "https://www.vxbilibili.com") \
                                                 .replace("http://bilibili.com", "https://www.vxbilibili.com") \
                                                 .replace("https://b23.tv", "https://vxb23.tv") \
                                                 .replace("http://b23.tv", "https://vxb23.tv")

                        try:
                            await message.delete()
                        except discord.Forbidden:
                            print("⚠️ 無法刪除 Bilibili 訊息")

                        await asyncio.sleep(1.5)
                        await message.channel.send(
                            f"🎮 由 @{sender} 提供的 Bilibili 影片：\n👉 {converted_url}"
                        )
                        break

client = AutoMediaBot()
client.run(TOKEN)
