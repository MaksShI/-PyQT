import argparse

import select
import socket
import sys
import json
import logging
import time

import logs.server_log_config
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, MESSAGE, MESSAGE_TEXT, SENDER, DESTINATION, RESPONSE_400, EXIT
from common.utils import get_message, send_message
from decos import ServerDecorate

SERVER_LOGGER = logging.getLogger('server')


def process_message(message, names, listen_socks):
    if message[DESTINATION] in names and names[message[DESTINATION]] in listen_socks:
        send_message(names[message[DESTINATION]], message)
    elif message[DESTINATION] in names and names[message[DESTINATION]] not in listen_socks:
        raise ConnectionError
    else:
        SERVER_LOGGER.critical(f'Пользователь {message[DESTINATION]} не зарегестрирован')


@ServerDecorate()
def process_client_message(message, messages_list, client, clients, names):
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message:
        if message[USER][ACCOUNT_NAME] not in names.keys():
            names[message[USER][ACCOUNT_NAME]] = client
            send_message(client, {RESPONSE: 200})
        else:
            response = RESPONSE_400
            response[ERROR] = 'Имя уже занято'
            send_message(client, response)
            clients.remove(client)
            client.close()
        return
    elif ACTION in message and message[ACTION] == MESSAGE and DESTINATION in message \
            and TIME in message and SENDER in message and MESSAGE_TEXT in message:

        messages_list.append(message)
        return
    elif ACTION in message and message[ACTION] == EXIT and ACCOUNT_NAME in message:
        clients.remove(names[message[ACCOUNT_NAME]])
        names[message[ACCOUNT_NAME]].close()
        del names[message[ACCOUNT_NAME]]
        return
    else:
        response = RESPONSE_400
        response[ERROR] = 'Запрос некорректен'
        send_message(client, response)
        return


@ServerDecorate()
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p
    if not 1023 < listen_port < 65536:
        SERVER_LOGGER.critical(f'Ошибка порта на клиенте, {listen_port}')
        sys.exit(1)

    return listen_address, listen_port


def main():
    listen_address, listen_port = arg_parser()
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    transport.settimeout(0.5)

    clients = []
    messages = []

    names = dict()

    transport.listen(MAX_CONNECTIONS)
    while True:
        try:
            client, client_address = transport.accept()
        except OSError:
            pass
        else:
            clients.append(client)

        recv_data_lst = []
        send_data_lst = []
        err_lst = []
        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass
        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    process_client_message(get_message(client_with_message), messages, client_with_message, clients,
                                           names)

                except Exception:
                    clients.remove(client_with_message)
        for i in messages:
            try:
                process_message(i, names, send_data_lst)
            except Exception:
                no_user_dict = RESPONSE_400
                no_user_dict[ERROR] = f'Полюзователь {i[DESTINATION]} отключился от сервера'
                send_message(names[i[SENDER]], no_user_dict)
                del names[i[DESTINATION]]
        messages.clear()


if __name__ == '__main__':
    main()
