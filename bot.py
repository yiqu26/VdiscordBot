
import discord
import os

TOKEN = os.getenv("TOKEN")

class AutoIGBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True  # 開啟讀取訊息內容的權限
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)

    async def on_ready(self):
        print(f"✅ Bot 上線：{self.user}")
        try:
            await self.tree.sync()
        except Exception as e:
            print(f"❌ 指令同步失敗：{e}")

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        # 偵測 IG Reels 連結
        if "instagram.com/reel/" in message.content:
            for word in message.content.split():
                if "instagram.com/reel/" in word:
                    # 清除網址中可能的參數，例如 utm
                    clean_url = word.split("?")[0]
                    converted_url = clean_url.replace("https://www.instagram.com", "https://ddinstagram.com")\
                                             .replace("http://www.instagram.com", "https://ddinstagram.com")\
                                             .replace("https://instagram.com", "https://ddinstagram.com")\
                                             .replace("http://instagram.com", "https://ddinstagram.com")
                    await message.channel.send(f"🔁 已轉換 IG Reels 連結：\n{converted_url}")
                    break

client = AutoIGBot()

client.run(TOKEN)
