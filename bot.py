import discord
from discord import app_commands
import os

TOKEN = os.getenv("TOKEN")

class GGInstaBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f"✅ Bot 上線：{self.user}")
        try:
            await self.tree.sync()
        except Exception as e:
            print(f"❌ 指令同步失敗：{e}")

client = GGInstaBot()

@client.tree.command(name="ig", description="轉換 IG 連結成 g.ginstagram.com 可播放影片")
@app_commands.describe(url="請貼上 Instagram 的貼文或 Reels 網址")
async def ig(interaction: discord.Interaction, url: str):
    await interaction.response.defer()
    if "instagram.com" not in url:
        await interaction.followup.send("⚠️ 請貼上有效的 Instagram 網址")
        return

    # 將 IG 網址轉為 InstaFix 的 g.g 預覽方式
    new_url = url.replace("https://www.instagram.com", "https://www.ddinstagram.com")\
                 .replace("http://www.instagram.com", "https://www.ddinstagram.com")\
                 .replace("https://instagram.com", "https://ddinstagram.com")\
                 .replace("http://instagram.com", "https://ddinstagram.com")

    await interaction.followup.send(f"🎥 已轉換連結：\n{new_url}")

client.run(TOKEN)
