import asyncio

import discord_user
from discord_user import secret
from discord_user.types import Activity
from discord_user.types.device import ClientDevice
from discord_user.types.presence import Presence

# например запуска с прокси и устройством
client = discord_user.Client(secret_token=secret.auth_token_discord_2)

@client.on_start
async def on_start():
    print("Пользователь запущен")

    # JSON данные для создания активности
    json_data = {
        'id': 'ed52e7003b57bc8',
        'created_at': 1723184107714,
        'name': 'Тест',
        'type': 0,
        'assets': {
            'large_image': 'mp:emojis/1212496120660365444.webp?format=webp&width=60&height=60'
        }
    }

    # Создание объекта Activity
    activity = Activity.from_json(json_data)

    # Установка активности пользователя
    await client.change_activity(activity=activity, status="online")


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(client.start_polling())
