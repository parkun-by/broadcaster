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
storage_cleaner = StorageCleaner(config.TEMP_FILES_PATH)


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

    caption = data['caption']
    photo_paths = data['photo_paths']
    coordinates = data['coordinates']
    await broadcaster.share(caption, photo_paths, coordinates)

    user_id = data['user_id']
    appeal_id = data['appeal_id']
    storage_cleaner.clean(user_id, appeal_id)


if __name__ == "__main__":
    main()
