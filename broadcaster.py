from twitter import Twitter
import logging

logger = logging.getLogger(__name__)


class Broadcaster:
    def __init__(self):
        self.twitter = Twitter()

    async def share(self,
                    title: str,
                    text: str,
                    photo_paths: list,
                    coordinates: list) -> None:
        logger.info('Шарим пост')

        try:
            await self.twitter.post(title, text, photo_paths, coordinates)
        except Exception:
            logger.exception("Twitter exception")
