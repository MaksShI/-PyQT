import sys
import json
import socket
import time
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_IP_ADDRESS, \
    DEFAULT_PORT
import logging
import logs.client_log_config
import logs.server_log_config

SERVER_LOGGER = logging.getLogger('server')
CLIENT_LOGGER = logging.getLogger('client')


class ClientDecorate:
    def __call__(self, func):
        def log(*args, **kwargs):
            CLIENT_LOGGER.debug(
                f'Была активирована функция {func.__name__} '
                f'Аргументы функции  {args}, {kwargs} '
                f'Функция была вызвана из модуля {func.__module__}', stacklevel=2)

            res = func(*args, **kwargs)
            return res

        return log


class ServerDecorate:
    def __call__(self, func):
        def log(*args, **kwargs):
            SERVER_LOGGER.debug(
                f'Была активирована функция {func.__name__} '
                f'Аргументы функции  {args}, {kwargs} '
                f'Функция была вызвана из модуля {func.__module__}', stacklevel=2)

            res = func(*args, **kwargs)
            return res

        return log
