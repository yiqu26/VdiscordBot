import discord
from discord import app_commands
import requests
import os

TOKEN = os.getenv("TOKEN")

class InstaBot(discord.Client):
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

client = InstaBot()

@client.tree.command(name="ig", description="取得 IG 貼文影片與資訊")
@app_commands.describe(url="貼上 Instagram 貼文或 Reels 的網址")
async def ig(interaction: discord.Interaction, url: str):
    await interaction.response.defer()

    if "instagram.com" not in url:
        await interaction.followup.send("⚠️ 請貼上有效的 Instagram 網址")
        return

    api_url = f"https://instafix.vercel.app/api/post?url={url}"
    try:
        res = requests.get(api_url, timeout=10)
        if res.status_code != 200:
            await interaction.followup.send("⚠️ InstaFix 回傳錯誤，請稍後再試")
            return

        data = res.json()
        caption = data.get("caption", "（無文字）")
        username = data.get("username", "未知使用者")
        likes = data.get("likes", 0)
        video_url = data.get("video", url)

        embed = discord.Embed(
            title=f"來自 @{username} 的 Instagram 貼文",
            description=caption,
            color=0xFF69B4
        )
        embed.add_field(name="❤️ 喜歡數", value=str(likes), inline=True)
        embed.add_field(name="▶️ 影片連結", value=video_url, inline=False)
        embed.set_footer(text="InstaFix 提供解析")

        await interaction.followup.send(embed=embed)

    except Exception as e:
        print("❌ 發生錯誤：", e)
        await interaction.followup.send("❌ 發生錯誤，請稍後再試")
client.run(TOKEN)
