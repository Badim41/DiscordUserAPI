import asyncio

from discord_user.types import Guild, Channel

import discord_user
from discord_user import secret
from discord_user.types.device import ClientDevice
from discord_user.types.message import DiscordMessage


client = discord_user.Client(secret_token=secret.auth_token_discord, device=ClientDevice.android)

check_user_ids = ["820845312217317397"]
check_channel_ids = ["1056451533623021582", "1062661622730084413"]

@client.message_handler
async def on_message(message: DiscordMessage):
    # message.text
    print(f"New message received: {message}")

@client.on_start
async def on_start():
    found_channels = []
    for guild in client.info.guilds.values():
        guild: Guild = guild

        for guild_channel in guild.channels.values():
            guild_channel: Channel = guild_channel

            if guild_channel.id in check_channel_ids:
                found_channels.append(guild_channel.id)

    for check_channel_id in check_channel_ids:
        if check_channel_id not in found_channels:
            print(f"[!] {check_channel_id} не найден!")

    print("Пользователь запущен")

@client.voice_status_handler
async def on_voice_status_update(data):
    print(f"voice update: {data}")


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(client.start_polling())
