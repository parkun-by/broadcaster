# Twitter
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

RABBIT_LOGIN = 'broadcaster'
RABBIT_PASSWORD = 'broadcaster'

RABBIT_AMQP_ADDRESS = \
    f'amqp://{RABBIT_LOGIN}:{RABBIT_PASSWORD}@{RABBIT_HOST}:{RABBIT_AMQP_PORT}'

BROADCAST_QUEUE = 'broadcast'


TEMP_FILES_PATH = '/tmp/temp_files_parkun'
PERSONAL_FOLDER = 'broadcaster'
