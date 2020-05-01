from broadcaster import Broadcaster
from storage_cleaner import StorageCleaner
from amqp_rabbit import Rabbit
import asyncio
import config
import json
import logging
import sys

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger("broadcaster")

broadcaster = Broadcaster()
storage_cleaner = StorageCleaner()


def main():
    loop = asyncio.get_event_loop()
    send_tasks = Rabbit()
    loop.run_until_complete(send_tasks.start(loop,
                                             broadcast,
                                             config.BROADCAST_QUEUE))
    loop.close()


async def broadcast(body) -> None:
    data = json.loads(body)
    logger.info(f'Сообщение от бота: {data}')

    storage_cleaner.create_folder()

    title = data.get('title', '') or ''
    text = data.get('text', '') or ''
    photo_paths = data.get('photo_paths', []) or []
    coordinates = data.get('coordinates', [None, None]) or [None, None]
    await broadcaster.share(title, text, photo_paths, coordinates)

    user_id = data['user_id']
    appeal_id = data['appeal_id']
    storage_cleaner.clean_bot_files(user_id=user_id, appeal_id=appeal_id)
    storage_cleaner.delete_folder()

if __name__ == "__main__":
    main()
