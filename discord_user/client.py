import json
import logging
import traceback
import zlib
from typing import List

import aiohttp

from .connections import ConnectionState
from .errors import SlashCommandException
from .types import SelfUserInfo
from .types.device import ClientDevice
from .types.event_type import get_event_code
from .types.message import DiscordMessage
from .types.presence import PresenceStatus, Presence
from .types.slash_command import SlashCommand, SlashCommandMessage

_log = logging.getLogger(__name__)


class Client:
    def __init__(
            self,
            secret_token,
            default_guild_ids: list = None,
            status=PresenceStatus.ONLINE,
            activity=None,
            device=ClientDevice.windows,
            afk=False,
            proxy_uri: str = None
    ):
        """
        :param secret_token: Секретный ключ аккаунта (Bearer <SECRET KEY>)
        :param default_guild_ids: Фильтр гильдий
        :param status: Статус (онлайн, офлайн, ...)
        :param activity: Активность
        :param device: Устройство (телефон, браузер ...)
        :param afk: bool, находится в AFK
        :param proxy_uri: str, SOCKS5 прокси
        """
        self._secret_token = secret_token
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
        self._default_guild_ids: List[int] = default_guild_ids or []
        self._status: str = status
        self._activity = activity if activity else []
        self._device = device
        self._afk: bool = afk
        self._proxy_uri: str = proxy_uri
        self._session = aiohttp.ClientSession()
        self._session.proxies = {'http': self._proxy_uri, 'https': self._proxy_uri}
        self._session.headers['authorization'] = self._secret_token

        self.info: SelfUserInfo = None

    # Декораторы для регистрации обработчиков
    async def start_polling(self):
        self._connection = ConnectionState(secret_token=self._secret_token, handler_method=self._handle_ws_event,
                                           status=self._status, device=self._device, afk=self._afk,
                                           proxy_uri=self._proxy_uri, activity=self._activity)
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
                    print("Decompression error:", e)
                    return
            elif isinstance(data, str):
                message = json.loads(data)
            elif data is None:
                raise Exception("data is NoneType")
            else:
                print(f"Message {data} with type type: {type(data)} ignored")
                return

            op = message.get('op')
            if op == 0:  # Dispatch event
                event = message.get('t')
                event_code = get_event_code(event)
                event_data = message['d']
                # print("message data:", event_data, event)

                if event == 'READY':
                    for handler in self._on_start_handler:
                        self.info = SelfUserInfo(event_data)
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
                elif event == 'PASSIVE_UPDATE_V2':
                    for handler in self._passive_update_v2_handlers:
                        await handler(event_data)
                elif event == 'SESSIONS_REPLACE':
                    for handler in self._session_replace_handlers:
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
                    print(f"Received unknown event: {event}", event_data)
                else:
                    # print(f"Event skip: {event}")
                    pass
            elif op == 10:
                self._connection._heartbeat_interval = message['d']['heartbeat_interval']
            elif op == 11:
                pass  # Операция, подтверждающая отправленный heartbeat
            else:
                print(f"Received operation: {op} with data: {message})")
        except Exception:
            print("Пропущена необработанная ошибка:")
            traceback.print_exc()

    # ================== POST REQUESTS =========================
    async def use_slash_command(self, slash_command: SlashCommand):
        url = 'https://discord.com/api/v9/interactions'
        headers = self._session.headers
        headers['content-type'] = 'multipart/form-data; boundary=----WebKitFormBoundary2X3yiJ1GSW21psnT'

        payload = f'------WebKitFormBoundary2X3yiJ1GSW21psnT\nContent-Disposition: form-data; name="payload_json"\n\n{slash_command.to_json()}\n------WebKitFormBoundary2X3yiJ1GSW21psnT--'

        # print("payload", payload)

        async with self._session.post(url, headers=headers, data=payload.encode("utf-8")) as response:
            if response.status != 204:
                text = None
                try:
                    text = await response.json()
                except Exception:
                    pass
                raise SlashCommandException(f"Ошибка при отправке слэш-команды: {text}. Код ошибки: {response.status}")

            print("interactions SUCCESS", await response.text())
