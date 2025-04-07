import nextcord
from nextcord.ext import commands

class 서버정보(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="서버정보", description="서버의 정보를 표시합니다.")
    async def serverinfo(self, interaction: nextcord.Interaction):
        if not interaction.guild:
            await interaction.response.send_message("이 명령어는 서버에서만 실행할 수 있습니다.", ephemeral=True)
            return

        guild = interaction.guild
        embed = nextcord.Embed(title=f"{guild.name} 서버 정보", color=nextcord.Color.purple())
        embed.add_field(name="서버 이름", value=guild.name, inline=False)
        embed.add_field(name="서버 ID", value=guild.id, inline=False)
        embed.add_field(name="서버 생성일", value=guild.created_at.strftime("%Y-%m-%d"), inline=False)
        embed.add_field(name="서버 멤버 수", value=guild.member_count, inline=False)

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(서버정보(bot))