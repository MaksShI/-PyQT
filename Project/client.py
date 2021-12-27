import argparse
import sys
import json
import socket
import threading
import time
import logging
from chardet import detect
import hashlib
import yaml
import logs.client_log_config
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, MESSAGE, MESSAGE_TEXT, SENDER, DESTINATION, SALT
from common.utils import get_message, send_message
from decos import ClientDecorate
from errors import ReqFieldMissingError, ServerError, IncorrectDataRecivedError

CLIENT_LOGGER = logging.getLogger('client')


def create_exit_message(usernam):
    sys.exit(1)


@ClientDecorate()
def message_form_server(sock, my_username):
    while True:
        try:
            message = get_message(sock)
            if ACTION in message and message[ACTION] == MESSAGE and \
                    SENDER in message and DESTINATION in message \
                    and MESSAGE_TEXT in message and message[DESTINATION] == my_username:
                print(f'\nПолучено сообщение от пользователя {message[SENDER]}:'
                      f'\n{message[MESSAGE_TEXT]}')
                CLIENT_LOGGER.info(f'Получено сообщение от пользователя {message[SENDER]}:'
                                   f'\n{message[MESSAGE_TEXT]}')
            else:
                CLIENT_LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')
        except IncorrectDataRecivedError:
            CLIENT_LOGGER.error(f'Не удалось декодировать полученное сообщение.')
        except (OSError, ConnectionError, ConnectionAbortedError,
                ConnectionResetError, json.JSONDecodeError):
            CLIENT_LOGGER.critical(f'Потеряно соединение с сервером.')
            break


@ClientDecorate()
def create_message(sock, account_name='Guest'):
    to_user = input('Введите получателя для отправки: ')
    message = input('Введите сообщение или "quit" для завершения: ')
    message_dict = {
        ACTION: MESSAGE,
        SENDER: account_name,
        DESTINATION: to_user,
        TIME: time.time(),
        MESSAGE_TEXT: message
    }
    CLIENT_LOGGER.debug(f'Сформировано сообщение {message_dict}')
    try:
        send_message(sock, message_dict)
    except:
        sys.exit(1)


def user_intaractive(sock, username):
    print_help()
    while True:
        command = input('Введите команду: ')
        if command == 'message':
            create_message(sock, username)
        elif command == 'help':
            print_help()
        elif command == 'exit':
            send_message(sock, create_exit_message(username))
            print("Завершение")
            time.sleep(1)
            break
        else:
            print('Команда не распознана, попробуйте снова.')


def password_is_valid(password):
    hash_object = hashlib.sha256(SALT.encode() + password.encode()).hexdigest()
    return hash_object


@ClientDecorate()
def create_presence(account_name='Guest'):
    # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    CLIENT_LOGGER.debug(f'создано сообщение{out}')
    return out

def registered():
    name = input('Придумайте имя пользователя: ')
    password = input('Придумайте пароль: ')
    password = password_is_valid(password)
    return name, password


def print_help():
    print('Поддерживаемые команды: ')
    print('message - отправить сообщение')
    print('help - вывусти подсказки по командам')
    print('exit - выход из программы')


@ClientDecorate()
def process_ans(message):
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            CLIENT_LOGGER.debug(f'получено сообщение {message}')
            return '200 : OK'
        CLIENT_LOGGER.debug(f'сообщение не получено {message}')
        return f'400 : {message[ERROR]}'
    return CLIENT_LOGGER.error(f'ошибка в сообщении клиента, {message}')


@ClientDecorate()
def process_response_ans(message):
    CLIENT_LOGGER.debug(f'Разбор приветственного сообщения от сервера {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200:OK'
        elif message[RESPONSE] == 400:
            raise ServerError(f'400:{message[ERROR]}')
    raise ReqFieldMissingError(RESPONSE)


@ClientDecorate()
def arg_parser():
    arguments = argparse.ArgumentParser()
    arguments.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    arguments.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    arguments.add_argument('-n', '--name', default=None, nargs='?')
    namespace = arguments.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_name = namespace.name
    if server_port < 1024 or server_port > 65535:
        CLIENT_LOGGER.critical(f'Ошибка порта на клиенте, {server_port}')
        sys.exit(1)

    return server_address, server_port, client_name



def main():
    # client.py 192.168.1.56 807
    with open('client.yaml', 'r', encoding='utf-8') as f_n:
        client_db = yaml.load(f_n, Loader=yaml.FullLoader)

    server_address, server_port, client_name = arg_parser()
    try:
        count = input('Желаете ли вы создать новый аккаунт(если у вас уже имееться аккаунт - просто пропустите это сообщение): ')
        if count != '':
            key, _KT = registered()
            client_db[key] = f'{_KT}'
            with open('client.yaml', 'w', encoding='utf-8') as f_n:
                yaml.dump(client_db, f_n)
        client_name = input('Введите имя пользователя: ')
        password = input('Введите ваш пароль: ')
        password = password_is_valid(password)
        if client_db[f'{client_name}'] == f'{password}':
            transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            transport.connect((server_address, server_port))
            send_message(transport, create_presence(client_name))
            answer = process_response_ans(get_message(transport))
        else:
            raise ServerError
    except json.JSONDecodeError:
        sys.exit(1)
    except ServerError as error:
        CLIENT_LOGGER.error('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)
    except ReqFieldMissingError as missing_error:
        sys.exit(1)
    except (ConnectionRefusedError, ConnectionError):
        sys.exit(1)
    else:
        receiver = threading.Thread(target=message_form_server, args=(transport, client_name))
        receiver.daemon = True
        receiver.start()
        user_interface = threading.Thread(target=user_intaractive, args=(transport, client_name))
        user_interface.daemon = True
        user_interface.start()
        while True:
            pass


if __name__ == '__main__':
    main()
