import nextcord
from nextcord.ext import commands
import psutil
import os
import sys
from datetime import datetime, timedelta

class Usage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="시스템", 
        description="서버의 CPU, RAM, 디스크 사용량 및 저장 공간을 확인합니다."
    )
    async def usage(self, interaction: nextcord.Interaction):
        # "불러오는 중..." 메시지 전송
        await interaction.response.send_message("🔄 불러오는 중... 잠시만 기다려 주세요.")

        # OS 정보
        os_name = os.name  # 'posix', 'nt' 등
        platform_info = os.uname() if os.name != 'nt' else "Windows 기반 OS"
        
        # CPU 정보
        cpu_usage = psutil.cpu_percent(interval=1)
        cpu_freq = psutil.cpu_freq()  # CPU 클럭 속도
        current_freq = cpu_freq.current if cpu_freq else "정보 없음"
        
        # RAM 정보 가져오기
        memory_info = psutil.virtual_memory()
        total_memory = memory_info.total / (1024 ** 3)
        used_memory = memory_info.used / (1024 ** 3)
        available_memory = memory_info.available / (1024 ** 3)

        # 디스크 정보 가져오기
        disk_path = 'C:\\'  # Linux/Unix에서는 '/'로 지정, Windows에서는 'C:\\' 등 적절히 변경
        disk_info = psutil.disk_usage(disk_path)
        total_disk = disk_info.total / (1024 ** 3)
        used_disk = disk_info.used / (1024 ** 3)
        free_disk = disk_info.free / (1024 ** 3)

        # 저장공간 상태
        storage_status = f"총 {total_disk:.2f} GB, 사용됨 {used_disk:.2f} GB, 남음 {free_disk:.2f} GB"

        # 디스크 I/O 속도
        disk_io = psutil.disk_io_counters()
        read_speed = disk_io.read_bytes / (1024 ** 2)  # MB
        write_speed = disk_io.write_bytes / (1024 ** 2)  # MB

        # 프로세스 수
        process_count = len(psutil.pids())

        # 업타임 계산
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        current_time = datetime.now()
        uptime = current_time - boot_time
        uptime_str = str(timedelta(seconds=uptime.total_seconds())).split('.')[0]  # 초 단위까지 표시

        # Python 버전 정보
        python_version = sys.version.split()[0]

        # 임베드 메시지 생성
        embed = nextcord.Embed(
            title="📊 서버 리소스 및 저장 공간 정보",
            color=0x00ff00
        )
        embed.add_field(name="🖥️ OS 정보", value=f"OS 이름: `{os_name}`\n플랫폼 정보: `{platform_info}`", inline=True)
        embed.add_field(name="🐍 Python 버전", value=f"`{python_version}`", inline=True)
        embed.add_field(name="⏱️ 서버 업타임", value=f"`{uptime_str}`", inline=True)
        embed.add_field(name="💻 CPU 상태", value=(
            f"사용량: `{cpu_usage}%`\n"
            f"클럭 속도: `{current_freq:.2f} MHz`"
        ), inline=True)
        embed.add_field(name="🧠 RAM 상태", value=(
            f"전체: `{total_memory:.2f} GB`\n"
            f"사용됨: `{used_memory:.2f} GB`\n"
            f"사용 가능: `{available_memory:.2f} GB`"
        ), inline=True)
        embed.add_field(name="💾 디스크 상태", value=storage_status, inline=True)
        embed.add_field(name="📈 디스크 I/O 속도", value=(
            f"읽기 속도: `{read_speed:.2f} MB`\n"
            f"쓰기 속도: `{write_speed:.2f} MB`"
        ), inline=True)
        embed.add_field(name="📋 프로세스 수", value=f"`{process_count}`", inline=True)
        embed.set_footer(text="데이터는 실시간으로 계산됩니다.")

        # 데이터 준비 후 최종 메시지 전송
        await interaction.edit_original_message(content=None, embed=embed)

def setup(bot):
    bot.add_cog(Usage(bot))