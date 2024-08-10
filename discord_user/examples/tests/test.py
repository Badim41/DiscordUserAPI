import asyncio
import datetime
import time

import discord_user
from discord_user import secret
from discord_user.types import CustomStatus, NoActivity
from discord_user.types.device import ClientDevice
from discord_user.types.message import DiscordMessage
from discord_user.types.presence import Presence


client = discord_user.Client(secret_token=secret.auth_token_discord_2, device=ClientDevice.android)

@client.on_start
async def on_start():
    print("Пользователь запущен")
    # await client.send_voice("1150573455960449118", audio_path=r"C:\Users\as280\Pictures\minecraft\soundPad\чих.mp3")
    await client.change_activity(activity=NoActivity(), status="online")

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(client.start_polling())
