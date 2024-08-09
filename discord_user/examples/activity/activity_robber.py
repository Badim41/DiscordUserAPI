import asyncio

import discord_user
from discord_user import secret
from discord_user.types import Activity
from discord_user.types.device import ClientDevice
from discord_user.types.presence import Presence

# например запуска с прокси и устройством
client = discord_user.Client(secret_token=secret.auth_token_discord)

from_user_id = secret.ds_id_1  # TODO SET SOME USER_ID


@client.on_start
async def on_start():
    print("Пользователь запущен")

@client.status_update_handler
async def on_presence_update(presence: Presence):
    if not presence.user.username:  # обновление статуса на сервере
        return
    if presence.user.id == from_user_id and len(presence.activities) > 0:
        print(
            f"change_activity {presence.user.username}, {presence.status}, {presence.client_status}, {presence.activities[0].to_dict()}")
        activity = presence.activities[0]

        await client.change_activity(activity=activity, status=presence.status)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(client.start_polling())
