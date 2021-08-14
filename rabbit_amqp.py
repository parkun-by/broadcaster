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
                connected = False
                await asyncio.sleep(pause)

                if pause < 30:
                    logger.info('Fail. Trying reconnect Rabbit.')
                    pause *= 2
                else:
                    logger.exception('Fail. Trying reconnect Rabbit.')

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
            channel: aio_pika.Channel = await self.connection.channel()

            await channel.declare_exchange(
                name=config.RABBIT_EXCHANGE,
                type=aio_pika.exchange.ExchangeType.DIRECT,
                durable=True,
                auto_delete=False,
                internal=False,
                passive=False
            )

            # Declaring queue
            queue = await channel.declare_queue(
                name=queue_name,
                durable=True,
                passive=False,
                auto_delete=False,
                arguments={
                    "x-queue-mode": "lazy"
                }
            )

            await queue.bind(
                exchange=config.RABBIT_EXCHANGE,
                routing_key=config.ROUTING_KEY_VIOLATION
            )

            logger.info("Подключились к раббиту")

            while True:
                async with queue.iterator(no_ack=False) as queue_iter:
                    async for message in queue_iter:
                        async with message.process():
                            await callback(message.body.decode())
