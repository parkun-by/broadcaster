# General
TEMP_FILES_PATH = '/tmp/temp_files_parkun'
PERSONAL_FOLDER = 'broadcaster'

BOLD = 'bold'
ITALIC = 'italic'
MONO = 'mono'
STRIKE = 'strike'

POST_URL = 'post_url'

# Twitter
TWITTER_ENABLED = False
CONSUMER_KEY = 'consumer_key'
CONSUMER_SECRET = 'consumer_secret'
ACCESS_TOKEN = 'access_token'
ACCESS_TOKEN_SECRET = 'access_token_secret'
MAX_TWI_CHARACTERS = 280
MAX_TWI_PHOTOS = 4
TWI_URL = 'twitter.com/SOME_TWITTER_ACCOUNT'

# RabbitMQ
RABBIT_HOST = 'localhost'
RABBIT_AMQP_PORT = '5672'
RABBIT_HTTP_PORT = '15672'

RABBIT_LOGIN = 'broadcaster'
RABBIT_PASSWORD = 'broadcaster'

RABBIT_AMQP_ADDRESS = \
    f'amqp://{RABBIT_LOGIN}:{RABBIT_PASSWORD}@{RABBIT_HOST}:{RABBIT_AMQP_PORT}'

RABBIT_HTTP_ADDRESS = \
    f'http://{RABBIT_LOGIN}:{RABBIT_PASSWORD}@{RABBIT_HOST}:{RABBIT_HTTP_PORT}'

BROADCAST_QUEUE = 'broadcast'
RABBIT_EXCHANGE_SHARING = 'sharing'
ROUTING_KEY = 'sharing_status'


# VK (see readme.md)
VK_ENABLED = False
VK_APP_ID = 'vk_app_id'  # just to remember
VK_GROUP_ID = 'vk_group_id'
VK_API_TOKEN = 'vk_api_token'

# Telegram
TG_ENABLED = False
TG_BOT_TOKEN = 'PUT_TOKEN_HERE'
TG_CHANNEL = '@channel_name'
