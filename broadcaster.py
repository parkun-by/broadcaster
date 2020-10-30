import logging
from asyncio.events import AbstractEventLoop

from telegram import Telegram
from twitter import Twitter
from vk import vk

logger = logging.getLogger(__name__)


class Broadcaster:
    def __init__(self, loop: AbstractEventLoop):
        self.twitter = Twitter()
        self.vk = vk()
        self.telegram = Telegram(loop)

    async def share(self,
                    title: dict,
                    body: dict,
                    photo_paths: list,
                    tg_photo_ids: list,
                    coordinates: list) -> None:
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
            await self.telegram.post(title_text,
                                     title_formatting,
                                     body_text,
                                     body_formatting,
                                     tg_photo_ids)
        except Exception:
            logger.exception("Telegram exception")

        try:
            await self.twitter.post(title_text,
                                    body_text,
                                    photo_paths,
                                    coordinates)
        except Exception:
            logger.exception("Twitter exception")
