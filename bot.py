import gspread
from oauth2client.service_account import ServiceAccountCredentials
import discord
from discord.ext import commands
import datetime

# Google Sheets APIの認証設定
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/kumis/Downloads/testa-427402-ca355962bf65.json', scope)
client = gspread.authorize(creds)

# スプレッドシートにアクセス
spreadsheet = client.open("テスト")
sheet = spreadsheet.sheet1

# Discord Botの設定
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 日付を取得
today = datetime.datetime.now().strftime("%m/%d")

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.listen()
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.strip()
    if content.startswith("出席　"):
        name = content[3:].strip()
        await process_attendance(message.channel, name, "〇")
    elif content.startswith("遅刻　"):
        parts = content.split()
        name = parts[1]
        time = " ".join(parts[2:])
        await process_attendance(message.channel, name, f"△ {time}")
    elif content.startswith("欠席　"):
        name = content[3:].strip()
        await process_attendance(message.channel, name, "")

async def process_attendance(channel, name: str, status: str):
    cell = sheet.find(name)
    if cell:
        row = cell.row
        col = sheet.find(today).col
        if status == "〇":
            sheet.update_cell(row, col, status)
            await channel.send(f"{name}さんの出席が記録されました。")
        elif status.startswith("△"):
            sheet.update_cell(row, col, status)
            await channel.send(f"{name}さんの遅刻が記録されました。")
        elif status == "":
            sheet.update_cell(row, col, status)
            await channel.send(f"{name}さんの欠席が記録されました。")
        else:
            await channel.send("無効なステータスです。出席、遅刻、欠席のいずれかを指定してください。")
    else:
        await channel.send(f"{name}さんが見つかりませんでした。")

bot.run('MTI1NDYzMTM0MjkyMzA1NTExNQ.GYS5v8.5pHODc-chGrqiltMtr7z4wY_vyJZ1aIqH7KGvY')
