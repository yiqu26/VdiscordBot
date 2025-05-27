import discord
from discord import app_commands
import os

TOKEN = os.getenv("TOKEN")

class SimpleBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f"✅ Bot 上線：{self.user}")
        try:
            await self.tree.sync()
        except Exception as e:
            print(f"❌ 指令同步失敗：{e}")

client = SimpleBot()

@client.tree.command(name="ig", description="轉換 IG 連結成 InstaFix 預覽")
@app_commands.describe(url="請貼上 Instagram 的貼文或 Reels 網址")
async def ig(interaction: discord.Interaction, url: str):
    await interaction.response.defer()
    if "instagram.com" not in url:
        await interaction.followup.send("⚠️ 請貼上有效的 Instagram 網址")
        return

    new_url = f"https://instafix.vercel.app/post?url={url}"
    await interaction.followup.send(f"🎥 點此觀看影片：\n{new_url}")

client.run(TOKEN)
