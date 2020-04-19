import config
import logging

# NOTE: the package name is peony and not peony-twitter
from peony import PeonyClient

logger = logging.getLogger(__name__)


class Twitter:
    def __init__(self):
        if config.ACCESS_TOKEN == 'access_token':
            self.client = None
        else:
            self.client = PeonyClient(
                consumer_key=config.CONSUMER_KEY,
                consumer_secret=config.CONSUMER_SECRET,
                access_token=config.ACCESS_TOKEN,
                access_token_secret=config.ACCESS_TOKEN_SECRET)

    def _pad(self, seq, target_length, padding):
        """Extend the sequence seq with padding (default: None) so as to make
        its length up to target_length. Return seq.
        """
        length = len(seq)
        seq.extend([padding] * (target_length - length))
        return seq

    def _get_chunks(self, my_list, number):
        for i in range(0, len(my_list), number):
            yield my_list[i:i + number]

    def _get_tweet_queue(self, photo_paths, caption):
        tweets_photos = list(self._get_chunks(photo_paths,
                                              config.MAX_TWI_PHOTOS))
        tweets_text = list(self._get_chunks(caption,
                                            config.MAX_TWI_CHARACTERS))

        tweet_count = max(len(tweets_photos), len(tweets_text))

        tweets_photos = self._pad(tweets_photos, tweet_count, [])
        tweets_text = self._pad(tweets_text, tweet_count, '')

        return list(zip(tweets_text, tweets_photos))

    async def post(self,
                   caption: str,
                   photo_paths: list,
                   coordinates: list) -> None:
        logger.info(f"Sending Tweet")

        if not self.client:
            return

        if not coordinates:
            coordinates = [None, None]

        tweet_queue = self._get_tweet_queue(photo_paths, caption)
        reply_to = None

        for tweet in tweet_queue:
            media_ids = []

            for file_path in tweet[1]:
                uploaded = await self.client.upload_media(file_path,
                                                          chunk_size=2**18,
                                                          chunked=True)
                media_ids.append(uploaded.media_id)

            tweet = await self.client.api.statuses.update.post(
                status=tweet[0],
                media_ids=media_ids,
                in_reply_to_status_id=reply_to,
                lat=coordinates[1],
                long=coordinates[0]
            )

            reply_to = tweet.data.id
