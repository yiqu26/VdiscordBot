import discord
import os

TOKEN = os.getenv("TOKEN")

class AutoIGBot(discord.Client):
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

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if "instagram.com/reel/" in message.content:
            for word in message.content.split():
                if "instagram.com/reel/" in word:
                    clean_url = word.split("?")[0]
                    converted_url = clean_url.replace("https://www.instagram.com", "https://ddinstagram.com")\
                                             .replace("http://www.instagram.com", "https://ddinstagram.com")\
                                             .replace("https://instagram.com", "https://ddinstagram.com")\
                                             .replace("http://instagram.com", "https://ddinstagram.com")

                    try:
                        await message.delete()
                    except discord.Forbidden:
                        print("⚠️ 沒有權限刪除訊息")
                    except discord.HTTPException as e:
                        print(f"⚠️ 刪除訊息失敗：{e}")

                    sender = message.author.display_name
                    await message.channel.send(
                        f"🔁 **由 @{sender} 提供的 IG Reels：**\n👉 {converted_url}"
                    )
                    break

client = AutoIGBot()
client.run(TOKEN)
