import logging
from asyncio.events import AbstractEventLoop

from config import TG_ENABLED, TWITTER_ENABLED, VK_ENABLED
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

        await self._share_to_vk(title_text, body_text, photo_paths)

        await self._share_to_tg(title_text,
                                title_formatting,
                                body_text,
                                body_formatting,
                                tg_photo_ids,
                                appeal_id,
                                user_id,
                                reply_id,
                                reply_type)

        await self._share_to_twi(title_text,
                                 body_text,
                                 photo_paths,
                                 coordinates)

    async def _share_to_vk(self, title: str, body: str, photo_paths: list):
        if not VK_ENABLED:
            logger.info("VK is disabled in config")
            return

        try:
            await self.vk.post(title, body, photo_paths)
            logger.info("VK - shared")
        except Exception:
            logger.exception("VK exception")

    async def _share_to_tg(self,
                           title_text: str,
                           title_formatting: list,
                           body_text: str,
                           body_formatting: list,
                           photo_ids: list,
                           appeal_id: int,
                           user_id: int,
                           reply_id: int,
                           reply_type: str):
        if not TG_ENABLED:
            logger.info("Telegram is disabled in config")
            return

        try:
            post_url = await self.telegram.post(title_text,
                                                title_formatting,
                                                body_text,
                                                body_formatting,
                                                photo_ids)

            logger.info("Telegram - shared")

            await self.rabbit.send_message(appeal_id,
                                           user_id,
                                           reply_id,
                                           reply_type,
                                           post_url)
        except Exception:
            logger.exception("Telegram exception")

    async def _share_to_twi(self,
                            title: str,
                            body: str,
                            photo_paths: list,
                            coordinates: list):
        if not TWITTER_ENABLED:
            logger.info("Twitter is disabled in config")
            return

        try:
            await self.twitter.post(title,
                                    body,
                                    photo_paths,
                                    coordinates)

            logger.info("Twitter - shared")
        except Exception:
            logger.exception("Twitter exception")
