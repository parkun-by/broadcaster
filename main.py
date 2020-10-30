import asyncio
import json
import logging
import sys

import config
from amqp_rabbit import Rabbit
from broadcaster import Broadcaster
from storage_cleaner import StorageCleaner

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

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

    coordinates = data.get('coordinates',
                           list([None, None])) or list([None, None])

    await broadcaster.share(title,
                            body,
                            photo_paths,
                            tg_photo_ids,
                            coordinates)

    user_id = data['user_id']
    appeal_id = data['appeal_id']
    storage_cleaner.clean_bot_files(user_id=user_id, appeal_id=appeal_id)
    storage_cleaner.delete_folder()

if __name__ == "__main__":
    main()
