import logging
import aio_pika
import config
import asyncio
from typing import Callable
from asyncio.events import AbstractEventLoop


logger = logging.getLogger(__name__)


class Rabbit:
    async def start(self,
                    loop: AbstractEventLoop,
                    callback: Callable,
                    queue: str):
        connected = False
        pause = 1

        while not connected:
            try:
                await self.connect(loop, callback, queue)
                connected = True
                pause = 1
            except Exception:
                logger.info('Fail. Trying reconnect Rabbit.')
                connected = False
                await asyncio.sleep(pause)

                if pause < 30:
                    pause *= 2

    async def connect(self,
                      loop: AbstractEventLoop,
                      callback: Callable,
                      queue_name: str) -> None:
        self.connection = await aio_pika.connect_robust(
            config.RABBIT_AMQP_ADDRESS,
            loop=loop
        )

        async with self.connection:
            # Creating channel
            channel = await self.connection.channel()

            # Declaring queue
            queue = await channel.declare_queue(
                queue_name,
                passive=True
            )

            logger.info("Подключились к раббиту")

            while True:
                async with queue.iterator(no_ack=False) as queue_iter:
                    async for message in queue_iter:
                        async with message.process():
                            await callback(message.body.decode())
