# Пример использования
# Пример использования класса DiscordUser
import asyncio
import datetime
import time

from discord_user import secret
import discord_user
from discord_user.types import Activity
from discord_user.types.device import ClientDevice
from discord_user.types.message import DiscordMessage
from discord_user.types.presence import Presence
from discord_user.types.slash_command import SlashCommand, SlashCommandMessage

proxy_uri = "socks5://localhost:5051"

client = discord_user.Client(secret_token=secret.auth_token_discord_2, proxy_uri=proxy_uri, device=ClientDevice.android)


@client.message_handler
async def on_message(message: DiscordMessage):
    # message.text
    print(f"New message received: {message}")

@client.on_start
async def on_start():
    print("Пользователь запущен")

    json_data_up_1 = {"type":2,"application_id":"464272403766444044","guild_id":"1069196218447691836","channel_id":"1070713643387330590","session_id":"de65ecd11b06f7454732482769257079","data":{"version":"891377101494681661","id":"891377101494681660","name":"up","type":1,"options":[],"application_command":{"id":"891377101494681660","type":1,"application_id":"464272403766444044","version":"891377101494681661","name":"up","description":"Апнуть сервер","options":[{"type":4,"name":"код","description":"Код капчи","description_localized":"Код капчи","name_localized":"код"}],"integration_types":[0],"global_popularity_rank":1,"description_localized":"Апнуть сервер","name_localized":"up"},"attachments":[]},"nonce":"1264783060335853568","analytics_location":"slash_ui"}
    # json_data_up_2 = {"type":2,"application_id":"464272403766444044","guild_id":"1069196218447691836","channel_id":"1070713643387330590","session_id":"de65ecd11b06f7454732482769257079","data":{"version":"891377101494681661","id":"891377101494681660","name":"up","type":1,"options":[{"type":4,"name":"код","value":1111}],"application_command":{"id":"891377101494681660","type":1,"application_id":"464272403766444044","version":"891377101494681661","name":"up","description":"Апнуть сервер","options":[{"type":4,"name":"код","description":"Код капчи","description_localized":"Код капчи","name_localized":"код"}],"integration_types":[0],"global_popularity_rank":1,"description_localized":"Апнуть сервер","name_localized":"up"},"attachments":[]},"nonce":"1264782141196075008","analytics_location":"slash_ui"}
    command = SlashCommand.from_dict(json_data_up_1, session_id=client.info.session_id)
    await client.use_slash_command(command)

@client.status_update_handler
async def on_presence_update(presence: Presence):
    if not presence.user.username: # обновление статуса
        return

    print(f"presence_update {presence.user.username}, {presence.status}, {presence.client_status}")

@client.slash_command_handler
async def on_slash_command_message(slash_command_message: SlashCommandMessage):
    # return
    if slash_command_message.embeds: # только с текстом
        if slash_command_message.author.id == "464272403766444044": # SD.C Monitoring
            if slash_command_message.embeds[0].image:
                print("capcha image:", slash_command_message.embeds[0].image.url)
                code = 1111 # TODO метод для решения капчи
                json_data_up_2 = {"type":2,"application_id":"464272403766444044","guild_id":"1069196218447691836","channel_id":"1070713643387330590","session_id":"de65ecd11b06f7454732482769257079","data":{"version":"891377101494681661","id":"891377101494681660","name":"up","type":1,"options":[{"type":4,"name":"код","value":code}],"application_command":{"id":"891377101494681660","type":1,"application_id":"464272403766444044","version":"891377101494681661","name":"up","description":"Апнуть сервер","options":[{"type":4,"name":"код","description":"Код капчи","description_localized":"Код капчи","name_localized":"код"}],"integration_types":[0],"global_popularity_rank":1,"description_localized":"Апнуть сервер","name_localized":"up"},"attachments":[]},"nonce":"1264782959282487296","analytics_location":"slash_ui"}
                command = SlashCommand.from_dict(json_data_up_2, session_id=client.info.session_id)
                await client.use_slash_command(command)
            else:
                print(f"Ответ [/up]: {slash_command_message.embeds[0].footer.text}")
    else:
        print(f"no embeds:, {slash_command_message.embeds}")
if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(client.start_polling())
