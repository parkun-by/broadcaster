import shutil
import os
import logging
import config

logger = logging.getLogger(__name__)


class StorageCleaner:
    def __init__(self):
        self.path = os.path.join(config.TEMP_FILES_PATH,
                                 config.PERSONAL_FOLDER)

    def create_folder(self):
        try:
            os.makedirs(self.path)
        except FileExistsError:
            pass

    def clean_bot_files(self, user_id: int, appeal_id: int):
        logger.info(f'Чистим файлы user_id {user_id} appeal_id {appeal_id}')

        try:
            shutil.rmtree(self._get_user_dir(user_id, appeal_id))
        except Exception:
            logger.exception("Can't delete files")

    def delete_folder(self):
        logger.info(f'Чистим файлы по пути: {self.path}')
        shutil.rmtree(self.path, ignore_errors=True)

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
