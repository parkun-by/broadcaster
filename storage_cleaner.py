import shutil
import os
import logging

logger = logging.getLogger(__name__)


class StorageCleaner:
    def __init__(self, storage_path: str):
        self.path = storage_path

    def clean(self, user_id: int, appeal_id: int):
        logger.info(f'Чистим файлы user_id {user_id} appeal_id {appeal_id}')

        shutil.rmtree(self._get_user_dir(user_id, appeal_id),
                      ignore_errors=True)

    def _get_user_dir(self, user_id: int, appeal_id: int) -> str:
        dir_path = self._get_user_dir_name(user_id, appeal_id)

        try:
            os.makedirs(dir_path)
            return dir_path
        except FileExistsError:
            return dir_path

    def _get_user_dir_name(self,
                           user_id: int,
                           appeal_id: int) -> str:
        return os.path.join(self.path, str(user_id), str(appeal_id))
