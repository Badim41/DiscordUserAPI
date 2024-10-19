import asyncio
import datetime
import sys

import discord_user
import secret
from discord_user.types import Activity, ActivityType, PresenceStatus, ClientDevice, EventType

# например запуска с прокси и устройством
proxy = "socks5://localhost:5051"  # Здесь указываем порт 5051, как в вашей команде SSH

client = discord_user.Client(secret_token=secret.auth_token_discord, device=ClientDevice.android, afk=True, proxy_uri=proxy)

# JSON данные для создания активности
json_data = {
    'id': 'ed52e7003b57bc8',
    'created_at': int(datetime.datetime.now().timestamp()) * 1000,
    'name': 'на да.. нет.. дет..',
    'type': ActivityType.WATCHING,
    'assets': {
        'large_image': 'mp:external/B1giPNB3AWgoIRAqkkYiXThuRyEtafUZw1NQuwnpieQ/https/yellowfire.ru/uploaded_files/yes-no-det.gif?width=600&height=600'
    },
    "timestamps": {
        "start": int(datetime.datetime.now().timestamp()) * 1000
    },
}

# Создание объекта Activity
activity = Activity.from_json(json_data)

@client.event_handler(EventType.SESSIONS_REPLACE)
async def on_session_replace(data):
    print("session update:", data)
    # Установка активности пользователя
    await client.change_activity(activity=activity, status=PresenceStatus.IDLE)


@client.on_start
async def on_start():
    print("Пользователь запущен")
    # Установка активности пользователя
    await client.change_activity(activity=activity, status=PresenceStatus.IDLE)
    await client._check_ip()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(client.start_polling())


