import asyncio
import json
import random
import traceback

import aiohttp
import websockets
from aiohttp_socks import ProxyConnector


class ConnectionState:
    def __init__(self, secret_token, handler_method, status, device, afk, proxy_uri, activity):
        self._secret_token = secret_token
        self._handler_method = handler_method
        self.websocket = None
        self._heartbeat_interval = None
        self._device = device
        self._status = status
        self._activity = activity
        self._afk = afk
        self._proxy_uri = proxy_uri

    async def _send_heartbeat(self):
        await asyncio.sleep(3)
        d_num = 23
        while True:
            if self._heartbeat_interval:
                await asyncio.sleep(self._heartbeat_interval / 1000 + random.random())

                heartbeat_payload = {"op": 1, "d": d_num}
                # print("send heartbeat", heartbeat_payload)

                await self.websocket.send_json(heartbeat_payload)

                d_num += random.randint(13, 17)  # честно не знаю как он считает
            else:
                await asyncio.sleep(3)
                print("No heartbeat!")

    async def connect(self):
        uri = "wss://gateway.discord.gg/?v=6&encoding=json"
        session_timeout = aiohttp.ClientTimeout(total=60)

        if self._proxy_uri:
            connector = ProxyConnector.from_url(self._proxy_uri)
        else:
            connector = aiohttp.TCPConnector()

        session = aiohttp.ClientSession(connector=connector, timeout=session_timeout)

        try:
            print(f"Connecting to {uri} with proxy {self._proxy_uri}" if self._proxy_uri else f"Connecting to {uri} without proxy")
            async with session.ws_connect(uri, max_msg_size=2 ** 22) as websocket:
                print("Connected to websocket")
                self.websocket = websocket
                await self.identify()
                await self._listen()
        except aiohttp.ClientConnectorError as e:
            print(f"Connection error: {e}")
        except aiohttp.ServerDisconnectedError as e:
            print(f"Server disconnected: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()
        finally:
            await session.close()
            print("Session closed")

    async def _listen(self):
        asyncio.create_task(self._send_heartbeat())
        while True:
            message = await self.websocket.receive()
            # print("message.data", message.data)
            await self._handler_method(message.data)

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
