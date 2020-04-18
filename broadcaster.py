from twitter import Twitter
import logging

logger = logging.getLogger(__name__)


class Broadcaster:
    def __init__(self):
        self.twitter = Twitter()

    async def share(self,
                    caption: str,
                    photo_paths: list,
                    coordinates: list) -> None:
        logger.info('Шарим пост')

        try:
            await self.twitter.post(caption, photo_paths, coordinates)
        except Exception:
            logger.exception("Twitter exception")
