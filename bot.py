
import discord
from discord import app_commands
import os

TOKEN = os.getenv("TOKEN")

class SocialBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f"✅ Bot 上線：{self.user}")
        try:
            synced = await self.tree.sync()
            print(f"✅ 指令同步成功，共 {len(synced)} 個")
        except Exception as e:
            print(f"❌ 指令同步失敗：{e}")

client = SocialBot()

@client.tree.command(name="ig", description="轉換 Instagram 影片連結為可嵌入樣式")
@app_commands.describe(url="請貼上 Instagram 貼文或 Reels 連結")
async def ig(interaction: discord.Interaction, url: str):
    await interaction.response.defer()
    if "instagram.com" not in url:
        await interaction.followup.send("⚠️ 請貼上有效的 Instagram 網址")
        return
    gallery_url = (
        url.replace("https://www.instagram.com", "https://g.ddinstagram.com")
           .replace("http://www.instagram.com", "https://g.ddinstagram.com")
           .replace("https://instagram.com", "https://g.ddinstagram.com")
           .replace("http://instagram.com", "https://g.ddinstagram.com")
    )
    await interaction.followup.send(f"📸 轉換完成：\n{gallery_url}")

@client.tree.command(name="fb", description="轉交 Facebook 影片連結給下載服務")
@app_commands.describe(url="請貼上 Facebook 影片連結")
async def fb(interaction: discord.Interaction, url: str):
    await interaction.response.defer()
    if "facebook.com" not in url:
        await interaction.followup.send("⚠️ 請貼上有效的 Facebook 影片網址")
        return
    download_link = f"https://fdownloader.net/download/?url={url}"
    await interaction.followup.send(f"🔗 點擊這裡下載影片：\n{download_link}")

client.run(TOKEN)
