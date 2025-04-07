import nextcord
from nextcord.ext import commands
import os

class DevCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.developer_id = int(os.getenv('DEVELOPER_ID'))
        self.additional_users = []

    async def check_if_authorized(self, interaction: nextcord.Interaction) -> bool:
        if interaction.user.id != self.developer_id and interaction.user.id not in self.additional_users:
            await interaction.response.send_message("⛔ 이 명령어를 사용할 권한이 없습니다.", ephemeral=True)
            return False
        return True

    @nextcord.slash_command(description="추가된 사용자에게 권한을 부여합니다 (개발자 전용)")
    async def 사용자추가(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = nextcord.SlashOption(
            name="사용자_이름",
            description="권한을 부여할 디스코드 사용자",
            required=True
        ),
    ):
        if interaction.user.id != self.developer_id:
            await interaction.response.send_message("⛔ 이 명령어는 개발자만 사용할 수 있습니다.", ephemeral=True)
            return

        user_id = member.id

        if user_id in self.additional_users:
            await interaction.response.send_message(f"✅ 사용자 `{member.display_name}` (ID: {user_id})는 이미 권한이 있습니다.", ephemeral=True)
            return

        self.additional_users.append(user_id)
        await interaction.response.send_message(f"✅ 사용자 `{member.display_name}` (ID: {user_id})에게 권한이 부여되었습니다.", ephemeral=True)

    @nextcord.slash_command(description="모든 Cog를 다시 로드합니다 (개발자 및 권한 있는 사용자 전용)")
    async def cog리로드(self, interaction: nextcord.Interaction):
        if not await self.check_if_authorized(interaction):
            return

        success_cogs = []
        failed_cogs = []

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                cog_name = filename[:-3]
                try:
                    self.bot.reload_extension(f'cogs.{cog_name}')
                    success_cogs.append(cog_name)
                except Exception as e:
                    failed_cogs.append(f"{cog_name} ({str(e)})")

        embed = nextcord.Embed(
            title="🔄 전체 Cog 리로드 결과",
            color=0x2ECC71 if not failed_cogs else 0xE74C3C
        )
        
        if success_cogs:
            embed.add_field(
                name="✅ 성공한 Cog",
                value="```\n" + "\n".join(success_cogs) + "```",
                inline=False
            )
        
        if failed_cogs:
            embed.add_field(
                name="❌ 실패한 Cog",
                value="```\n" + "\n".join(failed_cogs) + "```",
                inline=False
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)

def setup(bot): 
    bot.add_cog(DevCommands(bot))
