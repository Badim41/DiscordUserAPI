import asyncio

from discord_tools.timer import Time_Count

import discord_user
from discord_user import secret
from discord_user.types import EventType, DiscordMessage, ClientDevice
from discord_user.types.slash_command import SlashCommand, SlashCommandMessage
from ds_capcha.capcha_api import CapchaSolver


auth_token_discord = secret.auth_token_discord_2 # TODO set guild_id
app_session_reka = secret.reka_session # TODO set guild_id
guild_id = secret.test_guild_id # TODO set guild_id
channel_id = secret.test_channel_id # TODO set channel_id


client = discord_user.Client(secret_token=auth_token_discord, device=ClientDevice.android)

json_data_up_1 = {"type": 2, "application_id": "464272403766444044", "guild_id": guild_id,
                  "channel_id": channel_id, "session_id": "de65ecd11b06f7454732482769257079",
                  "data": {"version": "891377101494681661", "id": "891377101494681660", "name": "up", "type": 1,
                           "options": [], "application_command": {"id": "891377101494681660", "type": 1,
                                                                  "application_id": "464272403766444044",
                                                                  "version": "891377101494681661", "name": "up",
                                                                  "description": "Апнуть сервер", "options": [
                              {"type": 4, "name": "код", "description": "Код капчи",
                               "description_localized": "Код капчи", "name_localized": "код"}],
                                                                  "integration_types": [0], "global_popularity_rank": 1,
                                                                  "description_localized": "Апнуть сервер",
                                                                  "name_localized": "up"}, "attachments": []},
                  "nonce": "1264783060335853568", "analytics_location": "slash_ui"}
json_data_like = {"type": 2, "application_id": "575776004233232386", "guild_id": guild_id,
                  "channel_id": channel_id, "session_id": "bc2f4da45870f9f77b21d5d50cd766ba",
                  "data": {"version": "1209947057977163807", "id": "788801838828879933", "name": "like", "type": 1,
                           "options": [], "application_command": {"id": "788801838828879933", "type": 1,
                                                                  "application_id": "575776004233232386",
                                                                  "version": "1209947057977163807", "name": "like",
                                                                  "description": "Boost the server's ranking",
                                                                  "description_default": "Boost the server's ranking",
                                                                  "dm_permission": True, "integration_types": [0],
                                                                  "global_popularity_rank": 1, "options": [],
                                                                  "description_localized": "Поднять сервер в рейтинге",
                                                                  "name_localized": "like"}, "attachments": []},
                  "nonce": "1267352222442717184", "analytics_location": "slash_ui"}
json_data_bump_1 = {"type": 2, "application_id": "315926021457051650", "guild_id": guild_id,
                    "channel_id": channel_id, "session_id": "bc2f4da45870f9f77b21d5d50cd766ba",
                    "data": {"version": "956435492398841859", "id": "956435492398841858", "name": "bump", "type": 1,
                             "options": [], "application_command": {"id": "956435492398841858", "type": 1,
                                                                    "application_id": "315926021457051650",
                                                                    "version": "956435492398841859", "name": "bump",
                                                                    "description": "Increase rank of your server",
                                                                    "integration_types": [0],
                                                                    "global_popularity_rank": 1, "options": [],
                                                                    "description_localized": "Increase rank of your server",
                                                                    "name_localized": "bump"}, "attachments": []},
                    "nonce": "1267360098796175360", "analytics_location": "slash_ui"}

proxy_uri = "socks5://localhost:5051"
proxies = {'http': proxy_uri, 'https': proxy_uri}

last_images = {}
error_dump_in_row = 0
error_up_in_row = 0

capcha_solver = CapchaSolver(app_session_reka=app_session_reka, proxies=proxies)


@client.on_start
async def on_start():
    async def send_command():
        command_1 = SlashCommand.from_dict(json_data_bump_1, session_id=client.info.session_id)
        await client.use_slash_command(command_1)

        await asyncio.sleep(5)

        command_2 = SlashCommand.from_dict(json_data_up_1, session_id=client.info.session_id)
        await client.use_slash_command(command_2)

        await asyncio.sleep(5)

        command_3 = SlashCommand.from_dict(json_data_like, session_id=client.info.session_id)
        
        await client.use_slash_command(command_3)

    print("Пользователь запущен!")
    asyncio.ensure_future(send_command())

@client.slash_command_handler
async def on_slash_command_message(slash_command_message: SlashCommandMessage):
    if slash_command_message.embeds:  # только с текстом
        if slash_command_message.author.id == "464272403766444044":  # /up
            await solve_up(slash_command_message)
        elif slash_command_message.author.id == "575776004233232386":  # /like
            await solve_like(slash_command_message)
        elif slash_command_message.author.id == "315926021457051650":  # /dump
            await solve_dump(slash_command_message)



@client.message_handler
async def on_message(message: DiscordMessage):
    if message.author.id == "478321260481478677":  # Bump Reminder
        if "/up" in message.text:
            command = SlashCommand.from_dict(json_data_up_1, session_id=client.info.session_id)
        elif "/bump" in message.text:
            command = SlashCommand.from_dict(json_data_bump_1, session_id=client.info.session_id)
        elif "/like" in message.text:
            command = SlashCommand.from_dict(json_data_like, session_id=client.info.session_id)
            print("type /like")
            await asyncio.sleep(5, 15)
        else:
            return

        await client.use_slash_command(command)


async def solve_up(slash_command_message: SlashCommandMessage, attempts=5):
    global last_images, error_up_in_row
    first_embed = slash_command_message.embeds[0]
    if first_embed.image.url:
        for i in range(attempts):
            try:
                capcha_url = first_embed.image.url
                print("/up - capcha image:", capcha_url)

                timer = Time_Count()
                capcha_code, image_for_dataset = await asyncio.to_thread(capcha_solver.solve_capcha,
                                                                         capcha_url=capcha_url,
                                                                         delete_temp=False, chat_gpt4=attempts > 2)
                last_images['up'] = image_for_dataset

                print(f"Код из капчи: {capcha_code}, потрачено: {timer.count_time(ignore_error=True)}")

                json_data_up_2 = {"type": 2, "application_id": "464272403766444044", "guild_id": guild_id,
                                  "channel_id": channel_id, "session_id": "de65ecd11b06f7454732482769257079",
                                  "data": {"version": "891377101494681661", "id": "891377101494681660", "name": "up",
                                           "type": 1,
                                           "options": [{"type": 4, "name": "код", "value": capcha_code}],
                                           "application_command": {"id": "891377101494681660", "type": 1,
                                                                   "application_id": "464272403766444044",
                                                                   "version": "891377101494681661", "name": "up",
                                                                   "description": "Апнуть сервер", "options": [
                                                   {"type": 4, "name": "код", "description": "Код капчи",
                                                    "description_localized": "Код капчи", "name_localized": "код"}],
                                                                   "integration_types": [0],
                                                                   "global_popularity_rank": 1,
                                                                   "description_localized": "Апнуть сервер",
                                                                   "name_localized": "up"}, "attachments": []},
                                  "nonce": "1264782959282487296", "analytics_location": "slash_ui"}

                command = SlashCommand.from_dict(json_data_up_2, session_id=client.info.session_id)

                try:
                    test_text = f"Я думаю: {capcha_code}: {capcha_url}"
                    print("/up:", test_text)
                    await client.send_message(chat_id=channel_id, text=test_text)
                except:
                    print("error in send message in /up")

                await client.use_slash_command(command)
                error_up_in_row = 0
                return
            except Exception as e:
                error_up_in_row += 1
                if error_up_in_row >= attempts:
                    error_text = f"Не удалось решить /up спустя {attempts} попыток <@&1079868831016693832>"
                    await client.send_message(chat_id=channel_id, text=error_text)
                    error_up_in_row = 0
                    raise Exception(error_text)
                print(f"temp error in solve /up: {e}")
                command = SlashCommand.from_dict(json_data_up_1, session_id=client.info.session_id)
                await client.use_slash_command(command)
    elif "неверен" in first_embed.description:
        try:
            error_text = f"/up неуспешен: {first_embed.description}, {first_embed.footer.text}"
            await client.send_message(chat_id=channel_id, text=error_text)
        except:
            print("error in send message in /up")

        command = SlashCommand.from_dict(json_data_up_1, session_id=client.info.session_id)
        
        await client.use_slash_command(command)
        
        await asyncio.sleep(2)
    else:
        print(f"Ответ [/up]: {first_embed.description}")


async def solve_dump(slash_command_message: SlashCommandMessage, attempts=5):
    global last_images, error_dump_in_row
    first_embed = slash_command_message.embeds[0]
    if first_embed.image.url:
        for i in range(attempts):
            try:
                capcha_url = first_embed.image.url
                print("/bump - capcha image:", capcha_url)
                json_data_bump_2 = {"type": 3, "nonce": "1267361077574762496", "guild_id": guild_id,
                                    "channel_id": channel_id, "message_flags": 64,
                                    "message_id": slash_command_message.id, "application_id": "315926021457051650",
                                    "session_id": "bc2f4da45870f9f77b21d5d50cd766ba",
                                    "data": {"component_type": 2, "custom_id": "bump_captcha_answer_button"}}

                command_1 = SlashCommand.from_dict(json_data_bump_2, session_id=client.info.session_id)

                await client.use_slash_command(command_1)

                @client.event_handler(EventType.INTERACTION_SUCCESS)
                async def interaction_success_handler(data):
                    global error_dump_in_row
                    try:
                        print(f"DATA: {data}")
                        client._event_handlers[EventType.INTERACTION_SUCCESS].clear()  # отчистка хэндлера

                        capcha_code, image_for_dataset = await asyncio.to_thread(capcha_solver.solve_capcha,
                                                                                 capcha_url=capcha_url, delete_temp=False,
                                                                                 chat_gpt4=True)
                        timer = Time_Count()
                        print(f"Код из капчи: {capcha_code}, потрачено: {timer.count_time(ignore_error=True)}")
                        last_images['bump'] = image_for_dataset

                        json_data_bump_3 = {"type": 5, "application_id": "315926021457051650",
                                            "channel_id": channel_id,
                                            "guild_id": guild_id,
                                            "data": {"id": data['id'], "custom_id": "bump_captcha_answer_modal",
                                                     "components": [{"type": 1, "components": [
                                                         {"type": 4, "custom_id": "answer", "value": str(capcha_code)}]}]},
                                            "session_id": "bc2f4da45870f9f77b21d5d50cd766ba",
                                            "nonce": "1267362033355980800"}
                        print("json_data_bump_3", json_data_bump_3)
                        command_2 = SlashCommand.from_dict(json_data_bump_3, session_id=client.info.session_id)

                        test_text = f"Я думаю: {capcha_code}: {capcha_url}"
                        await client.send_message(chat_id=channel_id, text=test_text)

                        await client.use_slash_command(command_2)
                        error_dump_in_row = 0
                    except Exception as e:
                        error_dump_in_row += 1
                        if error_dump_in_row >= attempts:
                            error_text = f"Не удалось решить /dump спустя {attempts} попыток <@&1079868831016693832>"
                            await client.send_message(chat_id=channel_id, text=error_text)
                            error_dump_in_row = 0
                            raise Exception(error_text)
                        print(f"Error in solve /dump: {e}")
                        command = SlashCommand.from_dict(json_data_bump_1, session_id=client.info.session_id)
                        await client.use_slash_command(command)


                return
            except Exception as e:
                error_dump_in_row += 1
                if error_dump_in_row >= attempts:
                    error_text = f"Не удалось решить /dump спустя {attempts} попыток <@&1079868831016693832>"
                    await client.send_message(chat_id=channel_id, text=error_text)
                    raise Exception(error_text)
                print(f"Error in solve /dump: {e}")
                command = SlashCommand.from_dict(json_data_bump_1, session_id=client.info.session_id)
                await client.use_slash_command(command)
    elif ":x:" in first_embed.description:
        error_text = f"/bump неуспешен: {first_embed.description}, {first_embed.footer.text}"
        await client.send_message(chat_id=channel_id, text=error_text)

        command = SlashCommand.from_dict(json_data_bump_1, session_id=client.info.session_id)

        await client.use_slash_command(command)
        
        await asyncio.sleep(2)
    else:
        print(f"Ответ [/bump]: {first_embed.footer.text}")


async def solve_like(slash_command_message: SlashCommandMessage):
    first_embed = slash_command_message.embeds[0]
    if "Не так быстро" in first_embed.description:
        print("/like уже использован")
    elif "Вы успешно лайкнули сервер" in first_embed.description:
        print("/like успешен!")
    else:
        error_text = f"/like неуспешен: {first_embed.description}"
        await client.send_message(chat_id=channel_id, text=error_text)
        raise Exception(error_text)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(client.start_polling())
