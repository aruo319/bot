import os
import nextcord
import psutil
from nextcord.ext import commands, tasks
from dotenv import load_dotenv

# 환경 변수에서 토큰 로드
load_dotenv("token.env")
token = os.getenv("token")

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user}로 로그인되었습니다!")
    await bot.change_presence(
        activity=nextcord.Game(name="기본 상태 | 준비 완료 🎉")
    )
    update_server_status.start()  # 서버 상태 실시간 업데이트 시작

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "이벤트 시작" in message.content:
        await bot.change_presence(
            activity=nextcord.Activity(type=nextcord.ActivityType.playing, name="유저 이벤트 관리 중 🛠️")
        )
        await message.channel.send("상태가 '유저 이벤트 관리 중 🛠️'로 변경되었습니다!")
    elif "게임 시작" in message.content:
        await bot.change_presence(
            activity=nextcord.Game(name="사용자와 함께 게임 중 🎮")
        )
        await message.channel.send("상태가 '사용자와 함께 게임 중 🎮'로 변경되었습니다!")

    await bot.process_commands(message)

@tasks.loop(seconds=10)
async def update_server_status():
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    status_message = f"CPU: {cpu_usage}% | RAM: {ram_usage}%"

    await bot.change_presence(
        activity=nextcord.Activity(type=nextcord.ActivityType.watching, name=status_message)
    )

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f'로드됨: {filename[:-3]}')

@update_server_status.before_loop
async def before_update_server_status():
    await bot.wait_until_ready()

bot.run(token)