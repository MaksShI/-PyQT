import logging
import logging.config
import os
import sys
import logging.handlers
from common.variables import LOGGING_LEVEL, ENCODING

CLIENT_FORMATTER = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'config_test/client.log')

CLIENT_HANDLER = logging.StreamHandler(sys.stderr)
CLIENT_HANDLER.setFormatter(CLIENT_FORMATTER)
CLIENT_HANDLER.setLevel(logging.DEBUG)
LOG_FILE = logging.handlers.TimedRotatingFileHandler(PATH, encoding='utf-8', interval=1, when='midnight')
LOG_FILE.setFormatter(CLIENT_FORMATTER)


LOGGER = logging.getLogger('client')
LOGGER.addHandler(CLIENT_HANDLER)
LOGGER.addHandler(LOG_FILE)
LOGGER.setLevel(logging.ERROR)

if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.debug('Отладочная информация')
    LOGGER.info('Информационное сообщение')
