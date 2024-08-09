# Пример использования класса DiscordUser
import asyncio

import discord_user
from discord_user import secret
from discord_user.types import Activity
from discord_user.types.device import ClientDevice
from discord_user.types.message import DiscordMessage
from discord_user.types.presence import Presence

proxy_uri = "socks5://localhost:5051"

# например запуска с прокси и устройством
client = discord_user.Client(secret_token=secret.auth_token_discord_2, proxy_uri=proxy_uri, device=ClientDevice.android)


@client.message_handler
async def on_message(message: DiscordMessage):
    # message.text
    print(f"New message received: {message}")

@client.on_start
async def on_start():
    print("Пользователь запущен")

@client.status_update_handler
async def on_presence_update(presence: Presence):
    if not presence.user.username: # обновление статуса на сервере
        return

    print(f"presence_update {presence.user.username}, {presence.status}, {presence.client_status}")

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(client.start_polling())
