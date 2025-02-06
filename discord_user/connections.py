import asyncio
import json
import random
import traceback

import aiohttp
import websockets
from .global_logger import _log
from aiohttp import ClientWebSocketResponse
from aiohttp_socks import ProxyConnector


class ConnectionState:
    def __init__(self, secret_token, handler_method, status, device, afk, proxy_uri, activity):
        self._secret_token = secret_token
        self._handler_method = handler_method
        self.websocket: ClientWebSocketResponse = None
        self._heartbeat_interval = None
        self._device = device
        self._status = status
        self._activity = activity
        self._afk = afk
        self._proxy_uri = proxy_uri
        self._reconnect_delay = 3

    async def _send_heartbeat(self):
        await asyncio.sleep(3)
        d_num = 23
        while self.websocket and not self.websocket.closed:
            if self._heartbeat_interval:
                await asyncio.sleep(self._heartbeat_interval / 1000 + random.random())
                heartbeat_payload = {"op": 1, "d": d_num}
                try:
                    await self.websocket.send_json(heartbeat_payload)
                except Exception as e:
                    _log.error(f"Heartbeat error: {e}")
                    break  # Если ошибка, прерываем цикл
                d_num += random.randint(13, 17)  # честно не знаю как он считает
            else:
                await asyncio.sleep(3)
                _log.warning("No heartbeat!")

    async def connect(self):
        while True:  # для автоматического переподключения
            uri = "wss://gateway.discord.gg/?v=6&encoding=json"
            session_timeout = aiohttp.ClientTimeout(total=60)
            connector = ProxyConnector.from_url(self._proxy_uri) if self._proxy_uri else aiohttp.TCPConnector()
            session = aiohttp.ClientSession(connector=connector, timeout=session_timeout)

            try:
                _log.info(f"Connecting to {uri} with proxy {self._proxy_uri}" if self._proxy_uri else f"Connecting to {uri} without proxy")
                async with session.ws_connect(uri, max_msg_size=2 ** 40) as websocket:
                    print("Connected to websocket")
                    self.websocket = websocket
                    await self.identify()
                    await self._listen()
            except (aiohttp.ClientConnectorError, aiohttp.ServerDisconnectedError) as e:
                _log.error(f"Connection error: {e}")
            except Exception as e:
                _log.error(f"Unexpected error: {e}")
                traceback.print_exc()
            finally:
                await session.close()
                _log.info("Session closed. Reconnecting...")
                await asyncio.sleep(self._reconnect_delay)

    async def _listen(self):
        asyncio.create_task(self._send_heartbeat())
        _log.info("Start listening!")
        while self.websocket and not self.websocket.closed:
            try:
                message = await self.websocket.receive()
                if message.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
                    _log.info("WebSocket closed or error occurred")
                    break
                await self._handler_method(message.data)
            except Exception as e:
                _log.error("Error receiving message: {e}")
                break
        _log.error("WebSocket connection lost. Reconnecting...")

    async def identify(self):
        identify_payload = {
            "op": 2,
            "d": {
                "token": self._secret_token,
                "capabilities": 30717,
                "properties": self._device,
                "presence": {
                    "status": self._status,
                    "since": 0,
                    "activities": self._activity,
                    "afk": self._afk
                },
                "compress": False,
                "client_state": {
                    "guild_versions": {}
                }
            }
        }
        print("send json!")
        await self.websocket.send_json(identify_payload)
        # {"op": 3, "d": {"status": "idle", "since": 0, "activities": [
        #     {"name": "Custom Status", "type": 4, "state": "TEST-STATUS1", "timestamps": {"end": 1720612800000},
        #      "emoji": null}], "afk": false}}
        # {"op": 3, "d": {"status": "online", "since": 0, "activities": [
        #     {"name": "Custom Status", "type": 4, "state": "TEST-STATUS1", "timestamps": {"end": 1720612800000},
        #      "emoji": null}], "afk": false}}