import random
import nextcord
from nextcord.ext import commands

class 가위바위보(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.choices = {
            "가위": "✌️",
            "바위": "✊",
            "보": "🖐️"
        }

    @nextcord.slash_command(name="가위바위보", description="가위바위보 게임을 즐겨보세요!")
    async def play_rps(
        self,
        interaction: nextcord.Interaction,
        원하는것: str = nextcord.SlashOption(
            name="원하는것",
            description="가위, 바위, 보 중 하나를 선택해주세요!",
            choices=["가위", "바위", "보"]
        ),
    ):
        probabilities = {
            "win": 0.5,
            "draw": 0.3,
            "lose": 0.2
        }
        outcome = random.choices(
            population=["win", "draw", "lose"],
            weights=[probabilities["win"], probabilities["draw"], probabilities["lose"]],
            k=1
        )[0]
        bot_choice = self.calculate_bot_choice(원하는것, outcome)
        bot_choice_with_emoji = f"{bot_choice} {self.choices[bot_choice]}"
        result = self.get_result_message(outcome)
        await interaction.response.send_message(
            f"**당신의 선택:** {원하는것} {self.choices[원하는것]}\n"
            f"**봇의 선택:** {bot_choice_with_emoji}\n\n"
            f"**결과:** {result}"
        )

    def calculate_bot_choice(self, 원하는것, outcome):
        if outcome == "win":
            if 원하는것 == "가위":
                return "보"
            elif 원하는것 == "바위":
                return "가위"
            elif 원하는것 == "보":
                return "바위"
        elif outcome == "draw":
            return 원하는것
        elif outcome == "lose":
            if 원하는것 == "가위":
                return "바위"
            elif 원하는것 == "바위":
                return "보"
            elif 원하는것== "보":
                return "가위"

    def get_result_message(self, outcome):
        if outcome == "win":
            return "축하합니다! 당신이 이겼습니다! 🎉"
        elif outcome == "draw":
            return "무승부입니다!"
        elif outcome == "lose":
            return "아쉽지만, 봇이 이겼습니다! 😄"

def setup(bot):
    bot.add_cog(가위바위보(bot))
