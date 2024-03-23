import discord
import requests
from discord.ext import commands, tasks
import os
from keep_alive import keep_alive
keep_alive()
TOKEN = os.environ.get['TOKEN']

# 设置 FILECOIN 的 API URL
FILECOIN_API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=filecoin&vs_currencies=usd"

# 创建 Discord Bot 客户端
intents = discord.Intents.default()
intents.presences = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

# 定义一个获取 FILECOIN 价格的函数
def get_filecoin_price():
    response = requests.get(FILECOIN_API_URL)
    if response.status_code == 200:
        data = response.json()
        filecoin_price = data['filecoin']['usd']
        return f"$FIL Price: ${filecoin_price}"
    else:
        return "Failed to retrieve FILECOIN price"

# 定义一个定时任务来更新机器人的状态
@tasks.loop(minutes=10)  # 每 10 分钟更新一次状态
async def update_status():
    price = get_filecoin_price()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=price))

# 机器人启动时开始定时任务
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

    # 启动定时任务
    update_status.start()

# 运行机器人
bot.run(TOKEN)
