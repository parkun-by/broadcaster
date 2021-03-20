import asyncio
import json
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

import config
from broadcaster import Broadcaster
from rabbit_amqp import Rabbit
from storage_cleaner import StorageCleaner


Path("./logs").mkdir(parents=True, exist_ok=True)

file_handler_info = RotatingFileHandler("./logs/broadcaster_info.log",
                                        maxBytes=100000000,
                                        backupCount=5)
file_handler_info.setLevel(logging.INFO)

file_handler_error = RotatingFileHandler("./logs/broadcaster_error.log",
                                         maxBytes=10000000,
                                         backupCount=5)
file_handler_error.setLevel(logging.ERROR)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[file_handler_info, file_handler_error, stream_handler])

logger = logging.getLogger("broadcaster")
storage_cleaner = StorageCleaner()
broadcaster: Broadcaster


def main():
    loop = asyncio.get_event_loop()
    global broadcaster
    broadcaster = Broadcaster(loop)
    send_tasks = Rabbit()
    loop.run_until_complete(send_tasks.start(loop,
                                             broadcast,
                                             config.BROADCAST_QUEUE))
    loop.close()


async def broadcast(message_body: str) -> None:
    data = json.loads(message_body)
    logger.info(f'Сообщение от бота: {data}')

    storage_cleaner.create_folder()

    title: dict = data.get('title', dict()) or dict()
    body: dict = data.get('body', dict()) or dict()
    photo_paths = data.get('photo_paths', list()) or list()
    tg_photo_ids = data.get('tg_photo_ids', list()) or list()
    reply_id: int = data.get('reply_id', 0) or 0
    reply_type: str = data.get('reply_type', '') or ''

    coordinates = data.get('coordinates',
                           list([None, None])) or list([None, None])

    user_id: int = data['user_id']
    appeal_id: int = data['appeal_id']

    await broadcaster.share(user_id,
                            appeal_id,
                            title,
                            body,
                            photo_paths,
                            tg_photo_ids,
                            coordinates,
                            reply_id,
                            reply_type)

    storage_cleaner.clean_bot_files(user_id=user_id, appeal_id=appeal_id)
    storage_cleaner.delete_folder()

if __name__ == "__main__":
    main()
