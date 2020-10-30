import logging
from asyncio.events import AbstractEventLoop

from aiogram import Bot

from config import BOLD, ITALIC, MONO, STRIKE, TG_BOT_TOKEN, TG_CHANNEL
from photoitem import PhotoItem

logger = logging.getLogger("telegram")


class Telegram:
    """
    Sends messages to telegram channel
    """

    def __init__(self, loop: AbstractEventLoop) -> None:
        self._bot = Bot(token=TG_BOT_TOKEN, loop=loop)

    async def post(self,
                   title_text: str,
                   title_formatting: list,
                   body_text: str,
                   body_formatting: list,
                   photo_ids: list):
        title = self._get_formatted(title_text, title_formatting)
        body = self._get_formatted(body_text, body_formatting)
        text = f'{title}\n\n{body}'

        if photo_ids:
            await self._send_photos_group_with_caption(photo_ids, text)
        else:
            await self._bot.send_message(TG_CHANNEL, text, parse_mode='HTML')

    def _get_formatted(self, text: str, formatting: list) -> str:
        """
        Applies formatting to text.
        """
        for style in formatting:
            if style == BOLD:
                text = f'<b>{text}</b>'
            elif style == ITALIC:
                text = f'<i>{text}</i>'
            elif style == MONO:
                text = f'<code>{text}</code>'
            elif style == STRIKE:
                text = f'<s>{text}</s>'

        return text

    async def _send_photos_group_with_caption(self,
                                              photo_ids: list,
                                              caption='') -> None:
        photos = []

        for count, photo_id in enumerate(photo_ids):
            text = ''

            # add caption to first photo
            if count == 0:
                text = caption

            photo = PhotoItem('photo', photo_id, text)
            photos.append(photo)

        await self._bot.send_media_group(chat_id=TG_CHANNEL, media=photos)
