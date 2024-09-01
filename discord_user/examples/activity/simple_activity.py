import asyncio
import datetime
import sys

import discord_user
import secret
from discord_user.types import Activity, ActivityType, PresenceStatus, ClientDevice, EventType

# например запуска с прокси и устройством
client = discord_user.Client(secret_token=secret.auth_token_discord, device=ClientDevice.android, afk=True)

# JSON данные для создания активности
json_data = {
    'id': 'ed52e7003b57bc8',
    'created_at': int(datetime.datetime.now().timestamp()) * 1000,
    'name': 'на этого бесюкатого фенька',
    'type': ActivityType.WATCHING,
    'assets': {
        'large_image': 'mp:external/XUHTg9WU9tbN4CIV5h9am57_LFFPeSR4mroRFeErhzA/https/yellowfire.ru/uploaded_files/fara_spin.gif?width=375&height=375'
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


if __name__ == '__main__':
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.get_event_loop().run_until_complete(client.start_polling())
