# 1. Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться доступность сетевых узлов.
# Аргументом функции является список, в котором каждый сетевой узел должен быть представлен именем хоста или ip-адресом.
# В функции необходимо перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения («Узел доступен», «Узел недоступен»).
# При этом ip-адрес сетевого узла должен создаваться с помощью функции ip_address().
import subprocess
from random import randint
from subprocess import CREATE_NEW_CONSOLE


def ip_address():
    s = ''
    for i in range(0, 4):
        if i < 3:
            s += str(randint(0, 100)) + '.'
        else:
            s += str(randint(0, 100))
    print(s)
    return s


def host_ping(mass):
    k = 0
    while mass > k:
        try:
            k += 1
            ip = ip_address()
            subprocess.Popen(['ping', ip], creationflags=CREATE_NEW_CONSOLE)
            subprocess.check_output(f'ping {ip}')
            print('«Узел доступен»')
        except:
            print('«Узел недоступен»')


host_ping(10)
