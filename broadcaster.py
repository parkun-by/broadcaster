import logging
from asyncio.events import AbstractEventLoop

from http_rabbit import Rabbit
from telegram import Telegram
from twitter import Twitter
from vk import vk

logger = logging.getLogger(__name__)


class Broadcaster:
    def __init__(self, loop: AbstractEventLoop):
        self.twitter = Twitter()
        self.vk = vk()
        self.telegram = Telegram(loop)
        self.rabbit = Rabbit()

    async def share(self,
                    user_id: int,
                    appeal_id: int,
                    title: dict,
                    body: dict,
                    photo_paths: list,
                    tg_photo_ids: list,
                    coordinates: list,
                    reply_id: int,
                    reply_type: str) -> None:
        logger.info('Шарим пост')

        title_text = title.get('text', '') or ''
        title_formatting = title.get('formatting', list()) or list()

        body_text = body.get('text', '') or ''
        body_formatting = body.get('formatting', list()) or list()

        try:
            await self.vk.post(title_text, body_text, photo_paths)
        except Exception:
            logger.exception("VK exception")

        try:
            post_url = await self.telegram.post(title_text,
                                                title_formatting,
                                                body_text,
                                                body_formatting,
                                                tg_photo_ids)

            await self.rabbit.send_message(appeal_id,
                                           user_id,
                                           reply_id,
                                           reply_type,
                                           post_url)
        except Exception:
            logger.exception("Telegram exception")

        try:
            await self.twitter.post(title_text,
                                    body_text,
                                    photo_paths,
                                    coordinates)
        except Exception:
            logger.exception("Twitter exception")
