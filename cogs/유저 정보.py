import nextcord
from nextcord.ext import commands

class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="유저정보",
        description="유저의 정보를 불러옵니다."
    )
    async def user_info(
        self,
        ctx: nextcord.Interaction,
        멤버: nextcord.Member = nextcord.SlashOption(
            description="정보를 알고 싶은 멤버를 선택하세요.", required=False
        ),
    ):
        if 멤버 is None:
            멤버 = ctx.user

        # 배너 정보를 가져오기 위해 User 객체를 따로 가져옴
        try:
            user = await self.bot.fetch_user(멤버.id)  # ✅ 올바른 방식으로 유저 정보 가져오기
        except nextcord.NotFound:
            await ctx.send("유저 정보를 찾을 수 없습니다.")
            return

        # 멤버 상태 이모지 및 설명
        if 멤버.status == nextcord.Status.online:
            상태 = "🟢 온라인"
        elif 멤버.status == nextcord.Status.idle:
            상태 = "🌙 자리 비움"
        elif 멤버.status == nextcord.Status.dnd:
            상태 = "⛔ 방해 금지"
        else:
            상태 = "⚫ 오프라인"

        # 멤버 역할 리스트
        role_mentions = [role.mention for role in 멤버.roles if role != ctx.guild.default_role]
        roles_str = " ".join(role_mentions) if role_mentions else "역할 없음"

        # 활동 상태 메시지
        user_status = 멤버.activity
        status_message = user_status.name if user_status else "상태 메시지 없음"

        # 유저 타입 확인
        bot_status = "🤖 Bot" if 멤버.bot else "👤 User"

        # 임베드 생성
        embed = nextcord.Embed(
            title=f"**{멤버.display_name}**님의 정보",
            description=f"- {멤버}",
            color=nextcord.Color(0xD3851F),
        )
        embed.set_thumbnail(url=멤버.avatar.url)  # 프로필 이미지 추가

        # 배너 이미지 추가 (배너가 있는 경우)
        if user.banner:
            embed.set_image(url=user.banner.url)  # ✅ 올바른 방식으로 배너 추가
        else:
            embed.add_field(name="배너", value="배너 이미지가 없습니다.", inline=False)

        embed.add_field(name="ID", value=f"{멤버.id}", inline=True)
        embed.add_field(name="Type", value=f"{bot_status}", inline=True)
        embed.add_field(name="상태", value=f"{상태}", inline=True)
        embed.add_field(
            name="가입 시기",
            value=f"{멤버.created_at.strftime('%Y년 %m월 %d일 (%a) %H:%M:%S')}",
            inline=False,
        )
        embed.add_field(
            name="서버 가입 시기",
            value=f"{멤버.joined_at.strftime('%Y년 %m월 %d일 (%a) %H:%M:%S')}",
            inline=False,
        )
        embed.add_field(name="보유 역할", value=f"{roles_str}", inline=False)

        # 활동 상태 메시지 표시
        if user_status:
            embed.add_field(name="상태 메시지", value=status_message, inline=False)

        embed.set_footer(text="유저 정보는 실시간으로 불러옵니다.")

        # 임베드 전송
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(UserInfo(bot))
