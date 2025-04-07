import random
import nextcord
from nextcord.ext import commands
from datetime import datetime, timedelta

class 애인확률(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_used = {}  # 사용자별 마지막 명령어 사용 시간 저장

    @nextcord.slash_command(name="애인확률", description="애인이 생길 확률을 계산합니다! 하루에 한 번만 사용 가능.")
    async def 애인확률(self, interaction: nextcord.Interaction):
        user_id = interaction.user.id
        now = datetime.now()

        # 마지막 사용 기록 확인
        if user_id in self.last_used:
            last_time = self.last_used[user_id]
            if now - last_time < timedelta(days=1):
                remaining_time = timedelta(days=1) - (now - last_time)
                hours, seconds = divmod(remaining_time.seconds, 3600)
                minutes = seconds // 60
                await interaction.response.send_message(
                    f"❌ 이 명령어는 하루에 한 번만 사용할 수 있습니다!\n남은 시간: {remaining_time.days}일 {hours}시간 {minutes}분",
                    ephemeral=True
                )
                return

        # 확률 계산
        확률 = random.randint(0, 100)

        if 확률 >= 80:
            결과 = "🔥 매우 높은 확률! 곧 애인이 생길지도 몰라요!"
            색상 = 0xFF4500  # 주황색
        elif 50 <= 확률 < 80:
            결과 = "🙂 괜찮은 확률! 조금만 더 노력하면 가능성이 커요!"
            색상 = 0xFFD700  # 금색
        elif 20 <= 확률 < 50:
            결과 = "😅 애인이 생길 가능성이 낮지만, 긍정적인 태도가 중요해요!"
            색상 = 0x1E90FF  # 파란색
        else:
            결과 = "🙃 아직은 낮은 확률이네요. 새로운 사람들을 만나고 기회를 만들어보세요!"
            색상 = 0x696969  # 회색

        # 임베드 생성
        embed = nextcord.Embed(
            title="💖 애인 확률 계산기",
            description=f"애인이 생길 확률은 **{확률}%** 입니다!",
            color=색상
        )
        embed.add_field(name="🔮 결과", value=결과, inline=False)
        embed.set_footer(text="결과를 재미로만 봐주세요! 😊")

        # 마지막 사용 시간 업데이트
        self.last_used[user_id] = now

        # 임베드 전송
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(애인확률(bot))
