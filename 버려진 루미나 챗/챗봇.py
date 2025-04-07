import re
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import sqlite3
import os
import google.generativeai as genai



GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Google API 키가 설정되지 않았습니다. .env 파일에서 GOOGLE_API_KEY를 설정해주세요.")

genai.configure(api_key=GOOGLE_API_KEY)

MODEL_NAME = "gemini-2.0-flash-001"
try:
    model = genai.GenerativeModel(MODEL_NAME)
except Exception as e:
    model = None
    print(f"Gemini 모델 초기화 실패: {e}")

DATABASE_PATH = os.path.join(os.path.dirname(__file__), "user_data.db")

def connect_db():
    return sqlite3.connect(DATABASE_PATH)

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            discriminator TEXT,
            join_date TEXT,
            name TEXT,
            age INTEGER,
            interests TEXT,
            profile TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            message TEXT,
            response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def delete_old_chats(days=30):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM chat_history WHERE timestamp < datetime('now', ?)",
        (f"-{days} days",)
    )
    conn.commit()
    conn.close()

class UserCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        create_table()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if "루미나" in message.content.lower():
            trimmed_content = message.content.lower().strip()
            if trimmed_content == "루미나" or trimmed_content.endswith("루미나"):
                await message.channel.send("루미나 뒤에 할 말을 입력해주세요.")
                return

            previous_chats = self.get_previous_chats(message.author.id, limit=3)
            chat_context = "\n".join([f"사용자: {chat[0]}\n루미나: {chat[1]}" for chat in previous_chats])
            prompt = f"{chat_context}\n사용자: {message.content}\n루미나:"
            response = await self.generate_response(prompt, message.author.id)
            await message.channel.send(response)

    def get_previous_chats(self, user_id, limit=3):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT message, response FROM chat_history WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
            (user_id, limit)
        )
        rows = cursor.fetchall()
        conn.close()
        return rows

    def save_chat_history(self, user_id, message, response):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM chat_history WHERE user_id = ? AND message = ? AND response = ?",
            (user_id, message, response)
        )
        exists = cursor.fetchone()[0]
        if not exists:
            cursor.execute(
                "INSERT INTO chat_history (user_id, message, response) VALUES (?, ?, ?)",
                (user_id, message, response)
            )
            conn.commit()
        conn.close()

    async def generate_response(self, prompt, user_id):
        if not model:
            return "Gemini 모델이 초기화되지 않았습니다. 관리자에게 문의하세요."
        try:
            response = model.generate_content(contents=prompt).text.strip()
            self.save_chat_history(user_id, prompt, response)
            return response
        except Exception as e:
            if "429" in str(e):
                return "현재 사용량이 초과되었습니다. 잠시 후 다시 시도해주세요."
            print(f"Gemini API 오류: {e}")
            return "AI 응답 생성에 실패했습니다."



def setup(bot):
    bot.add_cog(UserCommands(bot))
