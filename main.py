import discord
from discord.ext import commands, tasks
import os
import requests
from keep_alive import keep_alive

keep_alive()

TOKEN = os.environ['TOKEN']

# 设置 FILECOIN 的 API URL
FILECOIN_API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
HEADERS = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': os.environ['CMC_API_KEY']  # Make sure you set your CoinMarketCap API key in the environment variable 'CMC_API_KEY'
}

# 创建 Discord Bot 客户端
intents = discord.Intents.default()
intents.presences = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

# 定义一个获取 FILECOIN 价格的函数
def get_filecoin_price():
    parameters = {
        'symbol': 'FIL'
    }
    response = requests.get(FILECOIN_API_URL, headers=HEADERS, params=parameters)
    if response.status_code == 200:
        data = response.json()
        filecoin_price = round(data['data']['FIL']['quote']['USD']['price'],3)
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
