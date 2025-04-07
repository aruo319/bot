import nextcord
from nextcord.ext import commands

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.categories = [
            {
                "name": "🎮 게임 관련",
                "commands": [
                    {"name": "가위바위보", "description": "가위바위보 게임을 즐기세요."},
                    {"name": "가위바위보대전", "description": "다른 사용자와 가위바위보 대결을 즐기세요!"},
                    {"name": "애인확률", "description": "애인을 가질 확률을 계산합니다."}
                ]
            },
            {
                "name": "🛠️ 정보 조회",
                "commands": [
                    {"name": "서버정보", "description": "현재 서버 정보를 확인합니다."},
                    {"name": "유저_정보", "description": "사용자의 정보를 조회합니다."},
                    {"name": "서버_사용량", "description": "서버의 자원 사용량을 확인합니다."},
                    {"name": "핑", "description": "봇의 응답 속도를 확인합니다."}
                ]
            },
            {
                "name": "💡 유틸리티",
                "commands": [
                    {"name": "번역기", "description": "다양한 언어를 번역합니다."}
                ]
            },
            {
                "name": "🎵 음악 관련",
                "commands": [
                    {"name": "!음악추가", "description": "음악을 대기열에 추가합니다. 예: `!음악추가 <음악 URL>`"},
                    {"name": "!음악대시보드", "description": "현재 대기열과 재생 중인 곡을 확인합니다."}
                ]
            }
        ]

    @nextcord.slash_command(name="도움말", description="카테고리를 탐색하며 도움말을 확인하세요.")
    async def help_command(self, interaction: nextcord.Interaction):
        # 호출한 사용자만 허용
        user = interaction.user
        current_category_index = 0
        embed = self.create_embed(current_category_index, user)
        await interaction.response.send_message(embed=embed, view=self.HelpView(self, current_category_index, user))

    def create_embed(self, category_index, user):
        """선택된 카테고리의 명령어를 보여주는 임베드 생성"""
        category = self.categories[category_index]
        embed = nextcord.Embed(
            title=f"📂 {category['name']} 도움말",
            description=f"{user.display_name}님만 사용 가능합니다.\n아래는 이 카테고리의 명령어들입니다:",
            color=nextcord.Color.green()
        )
        for command in category["commands"]:
            embed.add_field(
                name=f"🔹 {command['name']}",
                value=f"{command['description']}",
                inline=False
            )
        embed.set_footer(text=f"카테고리 {category_index + 1}/{len(self.categories)} | 화살표 버튼으로 탐색하세요!")
        return embed

    class HelpView(nextcord.ui.View):
        def __init__(self, cog, current_category_index, original_user):
            super().__init__(timeout=None)
            self.cog = cog
            self.current_category_index = current_category_index
            self.original_user = original_user

            # 이전/다음 버튼 추가
            self.add_item(self.NavigationButton("⬅️ 이전", -1, self))
            self.add_item(self.NavigationButton("➡️ 다음", 1, self))

            # 카테고리 드롭다운 추가
            self.add_item(self.CategoryDropdown(self))

        class NavigationButton(nextcord.ui.Button):
            def __init__(self, label, direction, view):
                super().__init__(label=label, style=nextcord.ButtonStyle.blurple)
                self.direction = direction
                self.view_reference = view

            async def callback(self, interaction: nextcord.Interaction):
                """버튼 클릭 처리"""
                if interaction.user != self.view_reference.original_user:
                    await interaction.response.send_message(
                        content="이 도움말은 다른 사용자가 생성한 세션입니다. 접근할 수 없습니다.",
                        ephemeral=True
                    )
                    return

                new_index = self.view_reference.current_category_index + self.direction
                if 0 <= new_index < len(self.view_reference.cog.categories):
                    self.view_reference.current_category_index = new_index
                    embed = self.view_reference.cog.create_embed(new_index, interaction.user)
                    await interaction.response.edit_message(embed=embed, view=self.view_reference)
                else:
                    await interaction.response.send_message(
                        content="이동할 수 없는 페이지입니다.", ephemeral=True
                    )

        class CategoryDropdown(nextcord.ui.Select):
            def __init__(self, view):
                options = [
                    nextcord.SelectOption(label=category["name"], description=f"{category['name']} 명령어")
                    for category in view.cog.categories
                ]
                super().__init__(placeholder="카테고리 선택", options=options)
                self.view_reference = view

            async def callback(self, interaction: nextcord.Interaction):
                """드롭다운 선택 처리"""
                if interaction.user != self.view_reference.original_user:
                    await interaction.response.send_message(
                        content="이 도움말은 다른 사용자가 생성한 세션입니다. 접근할 수 없습니다.",
                        ephemeral=True
                    )
                    return

                selected_index = next(
                    (index for index, category in enumerate(self.view_reference.cog.categories)
                     if category["name"] == self.values[0]), 0
                )
                self.view_reference.current_category_index = selected_index
                embed = self.view_reference.cog.create_embed(selected_index, interaction.user)
                await interaction.response.edit_message(embed=embed, view=self.view_reference)


def setup(bot):
    bot.add_cog(HelpCommand(bot))
