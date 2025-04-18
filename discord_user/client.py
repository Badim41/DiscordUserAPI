import json
import time
import traceback
import zlib
from typing import List

import aiofiles
import httpx

from discord_user.types import Emoji
from .connections import ConnectionState
from .errors import DiscordRequestError, InvalidTokenError
from .global_logger import _log
from .types import SelfUserInfo, Activity
from .types.device import ClientDevice
from .types.event_type import get_event_code
from .types.message import DiscordMessage
from .types.presence import PresenceStatus, Presence
from .types.slash_command import SlashCommand, SlashCommandMessage
from .utils.audio_utils import *
from .utils.mimetype_util import get_mimetype
from .utils.time_util import get_nonce


class Client:
    def __init__(
            self,
            secret_token,
            status=PresenceStatus.ONLINE,
            device=ClientDevice.windows,
            afk=False,
            proxy_uri: str = None,
            cookie: str = None
    ):
        """
        :param secret_token: Секретный ключ аккаунта (Bearer <SECRET KEY>)
        :param status: Статус (онлайн, офлайн, ...)
        :param device: Устройство (телефон, браузер ...)
        :param proxy_uri: str, SOCKS5 прокси
        """
        self._secret_token = secret_token
        self._discord_headers = {
            "accept": "*/*",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "authorization": self._secret_token,
            "origin": "https://discord.com",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
        }
        if cookie:
            self._discord_headers["cookie"] = cookie
        self._on_start_handler = []
        self._message_handlers = []
        self._slash_command_message_handlers = []
        self._message_update_handlers = []
        self._status_update_handlers = []
        self._event_handlers = {}
        self._super_supplement_handlers = []
        self._session_replace_handlers = []
        self._passive_update_v2_handlers = []
        self._voice_state_handlers = []
        self._connection: ConnectionState = None
        self._status: str = status
        self._activity = []
        self._device = device
        self._afk: bool = afk
        self._proxy_uri: str = proxy_uri
        # self._session = None
        if self._proxy_uri:
            self.proxies = {'http': self._proxy_uri, 'https': self._proxy_uri}
        else:
            self.proxies = None

        self.info: SelfUserInfo = None
        self._last_change_activity_time = 0

    # @property
    # def _session_connector(self):
    #     if self._proxy_uri:
    #         return ProxyConnector.from_url(self._proxy_uri)
    #     else:
    #         return aiohttp.TCPConnector(ssl=True, force_close=False)

    # Декораторы для регистрации обработчиков
    async def start_polling(self):
        self._connection = ConnectionState(secret_token=self._secret_token, handler_method=self._handle_ws_event,
                                           status=self._status, device=self._device, afk=self._afk,
                                           proxy_uri=self._proxy_uri, activity=self._activity)
        # asyncio.create_task(self._connection._process_messages())
        await self._connection.connect()

    def event_handler(self, event_code):
        def decorator(func):
            if event_code not in self._event_handlers:
                self._event_handlers[event_code] = []
            self._event_handlers[event_code].append(func)
            return func

        return decorator

    def message_handler(self, func):
        self._message_handlers.append(func)
        return func

    def voice_status_handler(self, func):
        self._voice_state_handlers.append(func)
        return func

    def slash_command_handler(self, func):
        self._slash_command_message_handlers.append(func)
        return func

    def message_update_handler(self, func):
        self._message_update_handlers.append(func)
        return func

    def on_start(self, func):
        self._on_start_handler.append(func)
        return func

    def status_update_handler(self, func):
        self._status_update_handlers.append(func)
        return func

    async def _handle_ws_event(self, data):
        try:
            if isinstance(data, bytes):
                try:
                    decompressed_data = zlib.decompress(data)
                    message = json.loads(decompressed_data.decode('utf-8'))
                except zlib.error as e:
                    _log.warning("Decompression error:", e)
                    return
            elif isinstance(data, str):
                message = json.loads(data)
            elif data is None:
                _log.warning("Reconnect to session...")
                await self._connection.connect()
                return
            elif data == 4004:
                raise InvalidTokenError("Неверный токен")
            else:
                _log.debug(f"Message {data} with type type: {type(data)} ignored")
                return

            op = message.get('op')
            if op == 0:  # Dispatch event
                event = message.get('t')
                event_code = get_event_code(event)
                event_data = message['d']
                # print("message data:", event_data, event)

                if event == 'READY':
                    _log.log(msg=f"Уровень логирования: {_log.level}", level=_log.level)
                    self.info = SelfUserInfo(event_data)
                    for handler in self._on_start_handler:
                        await handler()
                elif event == 'MESSAGE_UPDATE':
                    for handler in self._message_update_handlers:
                        message = DiscordMessage(event_data)
                        await handler(message)
                elif event == 'MESSAGE_CREATE':
                    if event_data.get('interaction_metadata', None):  # slash command message
                        for handler in self._slash_command_message_handlers:
                            message = SlashCommandMessage(event_data)
                            await handler(message)
                    else:
                        for handler in self._message_handlers:
                            message = DiscordMessage(event_data)
                            await handler(message)
                elif event == 'VOICE_STATE_UPDATE':
                    for handler in self._voice_state_handlers:
                        await handler(event_data)
                elif event == 'PRESENCE_UPDATE':
                    for handler in self._status_update_handlers:
                        activity = Presence(event_data)
                        await handler(activity)
                elif event_code and event_code in self._event_handlers:
                    for handler in self._event_handlers[event_code]:
                        await handler(event_data)
                elif not event_code:
                    # Добавьте другие события, которые вам нужны
                    _log.debug(f"Received unknown event: {event}: {event_data}")
                else:
                    # print(f"Event skip: {event}")
                    pass
            elif op == 10:
                self._connection._heartbeat_interval = message['d']['heartbeat_interval']
            elif op == 11:
                pass  # Операция, подтверждающая отправленный heartbeat
            else:
                _log.debug(f"Received operation: {op} with data: {message})")
        except Exception:
            _log.warning("Пропущена необработанная ошибка:")
            traceback.print_exc()

    # ================== attachments =========================
    async def _get_upload_url(self, channel_id, file_path: str):
        url = f"https://discord.com/api/v9/channels/{channel_id}/attachments"

        files = [
            {
                "filename": os.path.basename(file_path),
                "file_size": os.path.getsize(file_path),
                "is_clip": False
            }
        ]

        payload = {
            "files": files
        }
        async with httpx.AsyncClient(
                http2=True,
                headers=self._discord_headers,
                proxies=self.proxies
        ) as session:
            response = await session.post(url, headers=self._discord_headers, json=payload)
            if response.status_code == 200:
                try:
                    response_json = response.json()
                    return response_json
                except Exception:
                    raise DiscordRequestError(
                        f"Ошибка при получении ссылки. Код ошибки: {response.status_code}"
                    )
            else:
                response_text = response.text
                raise DiscordRequestError(
                    f"Ошибка при получении ссылки. Статус ошибки: {response.status_code}: {response_text}"
                )

    async def _create_attachment(self, channel_id, file_path, mimetype=None):
        filename = os.path.basename(file_path)

        if not mimetype:
            mimetype = get_mimetype(file_path)

        # Чтение файла
        async with aiofiles.open(file_path, 'rb') as f:
            audio_data = await f.read()

        # Получение URL для загрузки
        json_data_upload = await self._get_upload_url(channel_id=channel_id, file_path=file_path)
        upload_url = json_data_upload['attachments'][0]['upload_url']

        # Формирование multipart файлового запроса
        files = {
            "file": (filename, audio_data, mimetype)
        }

        async with httpx.AsyncClient(
                http2=True,
                headers=self._discord_headers,
                proxies=self.proxies
        ) as client:
            response = await client.put(upload_url, headers=self._discord_headers, files=files)

            if response.status_code == 200:
                # Здесь можно дополнительно обработать текст ответа, если требуется
                _ = response.text  # если нужно прочитать ответ
                return json_data_upload
            else:
                raise DiscordRequestError(
                    f"Ошибка при создании attachment. Статус ошибки: {response.status_code}: {response.text}"
                )

    # ================== POST REQUESTS =========================
    async def use_slash_command(self, slash_command: SlashCommand, force_multipart_form_data=False):
        url = 'https://discord.com/api/v9/interactions'

        headers = self._discord_headers

        json_data = slash_command.to_json()
        if json.loads(json_data).get("type",
                                     None) == 2 or force_multipart_form_data:  # я не уверен, нужно ли вообще form_data
            headers['content-type'] = 'multipart/form-data; boundary=----WebKitFormBoundary2X3yiJ1GSW21psnT'
            payload = f'------WebKitFormBoundary2X3yiJ1GSW21psnT\nContent-Disposition: form-data; name="payload_json"\n\n{slash_command.to_json()}\n------WebKitFormBoundary2X3yiJ1GSW21psnT--'
        else:
            headers['content-type'] = 'application/json'
            payload = json_data
        # print("payload", payload)
        # print(f"SEND SLASH COMMAND: {json_data}")

        async with httpx.AsyncClient(
                http2=True,
                headers=self._discord_headers,
                proxies=self.proxies
        ) as session:
            response = await session.post(url, headers=headers, data=payload)
            if response.status_code != 204:
                text = None
                try:
                    text = response.json()
                except Exception:
                    pass
                raise DiscordRequestError(
                    f"Ошибка при отправке слэш-команды: {text}. Код ошибки: {response.status_code}")

            # print("interactions SUCCESS", response.text)

    async def change_activity(self, activity: Activity, status: str, ignore_limit=False):
        if not ignore_limit and time.time() - self._last_change_activity_time < 20:
            return
        self._last_change_activity_time = time.time()
        if status not in PresenceStatus.status_list:
            raise TypeError(f"status должен быть одним из {PresenceStatus.status_list}")
        # {"op":3,"d":{"status":"online","since":0,"activities":[{"name":"Custom Status","type":4,"state":"ТЕСТ СТАТУС","timestamps":{"end":1738929599999},"emoji":null}],"afk":false}}
        activity_json = {
            "op": 3,
            "d": {
                "status": status,
                "since": 0,
                "activities": [activity.to_dict()],
                "afk": self._afk
            }
        }
        # print("set activity:", activity.to_dict())
        await self._connection.websocket.send_json(activity_json)

    async def send_voice(self, chat_id, audio_path) -> DiscordMessage:
        url = f"https://discord.com/api/v9/channels/{chat_id}/messages"

        audio_path_mp3 = convert_audio(original_audio_path=audio_path, audio_format="mp3")

        # Получение продолжительности аудио в секундах и формирование waveform
        duration_secs = get_audio_duration(audio_path_mp3)
        waveform_data = generate_waveform(audio_path_mp3)

        # print("waveform_data", waveform_data)
        # print("duration_secs", duration_secs)

        attachments_json_data = await self._create_attachment(channel_id=chat_id, file_path=audio_path_mp3)
        uploaded_filename = attachments_json_data['attachments'][0]['upload_filename']

        if not audio_path == audio_path_mp3:
            os.remove(audio_path_mp3)

        # Формирование данных для отправки
        payload = {
            "nonce": get_nonce(),
            "type": 0,
            "flags": 8192,
            "attachments": [{
                "id": "0",
                "filename": "voice-message.mp3",
                "uploaded_filename": uploaded_filename,
                "duration_secs": duration_secs,
                "waveform": waveform_data
            }]
        }

        async with httpx.AsyncClient(
                http2=True,
                headers=self._discord_headers,
                proxies=self.proxies
        ) as session:
            response = await session.post(url, headers=self._discord_headers, json=payload)
            if response.status_code == 200:
                try:
                    return DiscordMessage(response.json())
                except Exception as e:
                    raise DiscordRequestError(f"Ошибка при обработке ответа: {e}")
            else:
                raise DiscordRequestError(
                    f"Ошибка при отправке аудио. Статус ошибки: {response.status_code}: {response.text}")

    async def send_message(self, chat_id, text="", file_path=None, reply_message: DiscordMessage = None,
                           replied_user=False) -> DiscordMessage:
        url = f"https://discord.com/api/v9/channels/{chat_id}/messages"

        payload = {
            "mobile_network_type": "unknown",
            "type": 0,
            "content": text,
            "nonce": get_nonce(),
            "tts": False,
            "flags": 0
        }
        if reply_message:
            payload["message_reference"] = {
                "channel_id": reply_message.channel_id,
                "message_id": reply_message.message_id
            }
            if reply_message.guild_id:
                payload["message_reference"]["guild_id"] = reply_message.guild_id
            payload["allowed_mentions"] = {"parse": ["users", "roles", "everyone"], "replied_user": replied_user}

        if file_path:
            attachments_json_data = await self._create_attachment(channel_id=chat_id, file_path=file_path)
            uploaded_filename = attachments_json_data['attachments'][0]['upload_filename']
            payload["attachments"] = [{
                "id": "0",
                "filename": os.path.basename(file_path),
                "uploaded_filename": uploaded_filename
            }]

        _log.debug(f"payload send_message: {payload}")
        async with httpx.AsyncClient(
                http2=True,
                headers=self._discord_headers,
                proxies=self.proxies
        ) as session:
            response = await session.post(url, headers=self._discord_headers, json=payload)
            if response.status_code == 200:
                response_text = None
                try:
                    response_text = response.json()
                    return DiscordMessage(response_text)
                except Exception:
                    pass
                raise DiscordRequestError(
                    f"Ошибка при отправке сообщения: {response_text}. Код ошибки: {response.status_code}")
            else:
                raise DiscordRequestError(
                    f"Ошибка при отправке сообщения. Статус ошибки: {response.status_code}: {response.text}")

    async def send_typing(self, chat_id) -> int:
        url = f"https://discord.com/api/v9/channels/{chat_id}/typing"

        async with httpx.AsyncClient(
                http2=True,
                headers=self._discord_headers,
                proxies=self.proxies
        ) as session:
            response = await session.post(url, headers=self._discord_headers)
            if response.status_code == 204:
                return response.status_code
            else:
                raise DiscordRequestError(
                    f"Ошибка при отправке typing. Статус ошибки: {response.status_code}: {response.text}")

    async def delete_message(self, chat_id, message_id):
        url = f"https://discord.com/api/v9/channels/{chat_id}/messages/{message_id}"

        async with httpx.AsyncClient(
                http2=True,
                headers=self._discord_headers,
                proxies=self.proxies
        ) as session:
            response = await session.delete(url, headers=self._discord_headers)
            if response.status_code == 204:
                return
            else:
                raise DiscordRequestError(
                    f"Ошибка при удалении сообщения. Статус ошибки: {response.status_code}: {response.text}")

    async def set_reaction(self, chat_id, message_id, reaction: [Emoji, str]):
        if isinstance(reaction, str):
            emoji_str = reaction
        elif isinstance(reaction, Emoji):
            emoji_str = f"{reaction.name}:{reaction.id}/0"  # tatar:769298493922607187/0
        url = f"https://discord.com/api/v9/channels/{chat_id}/messages/{message_id}/reactions/{emoji_str}/@me?location=Message Reaction Picker&type=0"

        async with httpx.AsyncClient(
                http2=True,
                headers=self._discord_headers,
                proxies=self.proxies
        ) as session:
            response = await session.put(url, headers=self._discord_headers)
            if response.status_code == 204:
                return
            else:
                raise DiscordRequestError(
                    f"Ошибка при установки реакции. Статус ошибки: {response.status_code}: {response.text}")

    async def remove_reaction(self, chat_id, message_id, reaction: [Emoji, str]):
        if isinstance(reaction, str):
            emoji_str = reaction
        elif isinstance(reaction, Emoji):
            emoji_str = f"{reaction.name}:{reaction.id}/0"  # tatar:769298493922607187/0
        url = f"https://discord.com/api/v9/channels/{chat_id}/messages/{message_id}/reactions/{emoji_str}/@me?location=Message Inline Button&burst=false"

        async with httpx.AsyncClient(
                http2=True,
                headers=self._discord_headers,
                proxies=self.proxies
        ) as session:
            response = await session.delete(url, headers=self._discord_headers)
            if response.status_code == 204:
                return
            else:
                raise DiscordRequestError(
                    f"Ошибка при удалении реакции. Статус ошибки: {response.status_code}: {response.text}")

    async def get_messages(self, chat_id, limit: [int, str] = 50) -> List[DiscordMessage]:
        url = f"https://discord.com/api/v9/channels/{chat_id}/messages"

        querystring = {"limit": str(limit)}

        payload = ""

        async with httpx.AsyncClient(
                http2=True,
                headers=self._discord_headers,
                proxies=self.proxies
        ) as session:
            response = await session.get(url, headers=self._discord_headers, params=querystring)
            if response.status_code == 200:
                response_text = None
                try:
                    response_text = response.json()
                    return [DiscordMessage(json_data) for json_data in response_text]
                except Exception:
                    pass
                raise DiscordRequestError(
                    f"Ошибка при получении сообщений: {response_text}. Код ошибки: {response.status_code}")
            else:
                raise DiscordRequestError(
                    f"Ошибка при получении сообщений. Статус ошибки: {response.status_code}: {response.text}")

    async def _check_ip(self):
        async with httpx.AsyncClient(
                http2=True,
                proxies=self.proxies
        ) as session:
            # главное сюда 'session.headers['authorization'] = self._secret_token' не поставьте :)
            response = await session.get("http://icanhazip.com")
            if response.status_code == 200:
                text = response.text
                print("ip:", text)
                return text
            else:
                raise DiscordRequestError(
                    f"Ошибка при получении IP. Статус ошибки: {response.status_code}: {response.text}")
