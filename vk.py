import json
import logging
import aiohttp
from files_opener import FilesOpener
from typing import Tuple, Optional
import config

logger = logging.getLogger(__name__)


class vk:
    async def _request_get(self,
                           url: str,
                           params: dict) -> Tuple[Optional[dict], int]:
        async with aiohttp.ClientSession() as http_session:
            async with http_session.get(url, params=params) as response:
                status = response.status

                try:
                    response = await response.json(content_type=None)
                except json.JSONDecodeError:
                    logger.warning('Опять результат реквеста не смог в json')
                    response = None

                return response, status

    async def _request_post(self, url: str, data: dict) -> dict:
        async with aiohttp.ClientSession() as http_session:
            async with http_session.post(url, data=data) as response:
                return await response.json(content_type=None)

    async def post(self, title: str, text: str, image_paths: list):
        if title:
            text = title + '\n\n' + text

        # Сначала нужно загрузть фотку на сервера ВК
        photos = await self._upload_images_to_wall(image_paths)

        # Потом получить её ID
        attachments = ','.join([
            'photo'+str(photo['owner_id'])+'_'+str(photo['id'])
            for photo in photos
        ])

        # И запостить на стену группы
        await self._post_to_wall(text, attachments)

    async def _upload_images_to_wall(self, paths: list) -> list:
        uploaded_photos = []

        if not paths:
            return uploaded_photos

        # получаем адрес сервера для заливания фото
        params = {
            'group_id': config.VK_GROUP_ID,
            'access_token': config.VK_API_TOKEN,
            'v': '5.95'
        }

        url = 'https://api.vk.com/method/photos.getWallUploadServer'

        response, status = await self._request_get(url, params)
        upload_server = response['response']['upload_url']

        # подготавливаем и заливаем фото
        with FilesOpener(paths, key_format='photo') as photos_files:
            for photo_file in photos_files:
                photo = {'photo': photo_file[1][1]}
                response = await self._request_post(upload_server, data=photo)

                params.update(response)
                url = 'https://api.vk.com/method/photos.saveWallPhoto'
                response, status = await self._request_get(url, params)

                uploaded_photos += response['response']

        logger.info('Результат загрузки фоток на стену: ' +
                    str(uploaded_photos))

        return uploaded_photos

    async def _post_to_wall(self, message='', attachments=''):
        params = {
            'owner_id': '-' + config.VK_GROUP_ID,
            'from_group': '1',
            'message': message,
            'attachments': attachments,
            'access_token': config.VK_API_TOKEN,
            'v': '5.95',
        }

        url = 'https://api.vk.com/method/wall.post'

        response, status = await self._request_get(url, params)

        if status == 200:
            logger.info('Успешно запостилось.')
        elif status == 414:
            logger.warning(
                'Слишком большая длина текста для постинга в ВК. ВК лох.')
        else:
            logger.error('Что-то пошло не так, код ошибки - ' + str(status))
