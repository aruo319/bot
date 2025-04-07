import nextcord
from nextcord.ext import commands
import time

class 핑(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="핑", description="핑을 확인합니다.")
    async def ping(self, interaction: nextcord.Interaction):
        start_time = time.time()
        await interaction.response.send_message("퐁!")
        end_time = time.time()

        rest_ping = round((end_time - start_time) * 1000)
        gateway_ping = round(self.bot.latency * 1000)

        embed = nextcord.Embed(title="핑 정보", color=nextcord.Color.blue())
        embed.add_field(
            name="루미나가 받아 치는데에 걸린 시간입니다!",
            value=f"REST 핑: {rest_ping}ms\nGateway 핑: {gateway_ping}ms",
            inline=False
        )

        await interaction.edit_original_message(embed=embed)

def setup(bot):
    bot.add_cog(핑(bot))