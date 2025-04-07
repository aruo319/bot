from googletrans import Translator
import nextcord
from nextcord.ext import commands

class 무료번역기(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.translator = Translator()

    @nextcord.slash_command(name="번역", description="Google Translate API를 이용해 텍스트를 번역합니다.")
    async def 번역(self, interaction: nextcord.Interaction, 원문: str, 대상언어: str):
        지원_언어 = ['ko', 'en', 'ja', 'fr', 'de', 'zh-cn', 'zh-tw', 'es', 'ru']
        
        if 대상언어 not in 지원_언어:
            await interaction.response.send_message(
                f"유효하지 않은 언어 코드입니다. 지원 언어: {', '.join(지원_언어)}", ephemeral=True
            )
            return
        
        try:
            번역_결과 = self.translator.translate(원문, dest=대상언어)  # 번역 작업
            번역된_텍스트 = 번역_결과.text
            await interaction.response.send_message(
                f"**번역 완료:**\n{번역된_텍스트}"
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ 번역 도중 오류가 발생했습니다: {e}", ephemeral=True
            )

def setup(bot):
    bot.add_cog(무료번역기(bot))
