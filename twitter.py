import logging
import os

from peony import PeonyClient
from PIL import Image, ImageDraw, ImageFont

import config

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

    def _prepare_pictures(self, current: list, text_to_pic: str) -> list:
        if text_to_pic:
            text_pic = self._text2png(text_to_pic)
            current.append(text_pic)

        return current

    def _text2png(self,
                  text: str,
                  width=1600) -> str:
        REPLACEMENT_CHARACTER = u'\uFFFD'
        NEWLINE_REPLACEMENT_STRING = ' ' + REPLACEMENT_CHARACTER + ' '
        FONTFULLPATH = "LiberationSerif-Regular.ttf"
        FONTSIZE = 50

        font = ImageFont.truetype(FONTFULLPATH, FONTSIZE)
        text = text.replace('\n', NEWLINE_REPLACEMENT_STRING)

        lines = []
        line = ""
        LEFTPADDING = 3
        RIGHTPADDING = 3

        for word in text.split():
            actual_width = width - RIGHTPADDING - LEFTPADDING

            if word == REPLACEMENT_CHARACTER:  # give a blank line
                # slice the white space in the begining of the line
                lines.append(line[1:])
                line = ""
            elif font.getsize(line + ' ' + word)[0] <= (actual_width):
                line += ' ' + word
            else:  # start a new line
                # slice the white space in the begining of the line
                lines.append(line[1:])
                line = ""

                # TODO: handle too long words at this point
                # for now, assume no word alone can exceed the line width
                line += ' ' + word

        if len(line) != 0:
            lines.append(line[1:])  # add the last line

        line_height = font.getsize(text)[1]
        img_height = line_height * (len(lines) + 1)

        BGCOLOR = "#FFF"
        img = Image.new("RGBA", (width, img_height), BGCOLOR)
        draw = ImageDraw.Draw(img)

        y = 0
        COLOR = "#000"

        for line in lines:
            draw.text((LEFTPADDING, y), line, COLOR, font=font)
            y += line_height

        PATH = os.path.join(config.TEMP_FILES_PATH,
                            config.PERSONAL_FOLDER,
                            'response.png')
        img.save(PATH)
        return PATH

    async def post(self,
                   caption: str,
                   text: str,
                   photo_paths: list,
                   coordinates: list) -> None:
        logger.info(f"Sending Tweet")

        if not caption and len(text) < config.MAX_TWI_CHARACTERS:
            caption = text
        else:
            self._prepare_pictures(photo_paths, text)

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
