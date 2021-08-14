from typing import Optional
import aiohttp
import config
import json

PERSISTENT = 2


class Rabbit:
    async def _send(self,
                    exchange_name: str,
                    routing_key: str,
                    body: dict) -> None:
        url = config.RABBIT_HTTP_ADDRESS + \
            f'/api/exchanges/%2F/{exchange_name}/publish'

        data = {
            'properties': {
                'delivery_mode': PERSISTENT,
            },
            'routing_key': routing_key,
            'payload': json.dumps(body),
            'payload_encoding': 'string'
        }

        async with aiohttp.ClientSession() as http_session:
            async with http_session.post(url, json=data) as response:
                if response.status != 200:
                    raise Exception(
                        f'Ошибка при отправке обращения: {response.reason}')

    async def send_message(self,
                           appeal_id: int,
                           user_id: int,
                           reply_id: int,
                           reply_type: str,
                           post_url: str) -> None:
        body = {
            'type': config.POST_URL,
            'appeal_id': appeal_id,
            'user_id': user_id,
            'reply_id': reply_id,
            'reply_type': reply_type,
            'post_url': post_url,
        }

        await self._send(config.RABBIT_EXCHANGE,
                         config.ROUTING_KEY_SHARING_STATUS,
                         body)
