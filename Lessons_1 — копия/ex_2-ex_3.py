# 2. Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона.
# Меняться должен только последний октет каждого адреса.
# По результатам проверки должно выводиться соответствующее сообщение.
import subprocess
from subprocess import CREATE_NEW_CONSOLE
from tabulate import tabulate

def return_str_in_mass(min_num, max_num):
    min_num = min_num.split('.')
    max_num = max_num.split('.')
    mass = ''
    mass = (min_num[0] + '.' + min_num[1] + '.' + min_num[2])
    alter_number = int(min_num[-1])
    number = int(max_num[-1])
    return mass, alter_number, number


def host_range_ping(min_num, max_num):
    count_True = []
    count_False = []
    all_variables = return_str_in_mass(min_num, max_num)
    for i in range(all_variables[1], all_variables[2] + 1):
        try:
            ip_address = all_variables[0] + '.' + str(i)
            print(f'Идет проверка ip адресса {ip_address}')
            subprocess.Popen(['ping', ip_address], creationflags=CREATE_NEW_CONSOLE)
            subprocess.check_output(f'ping {ip_address}')
            count_True.append(ip_address)
            print('«Узел доступен»')
        except:
            print('«Узел недоступен»')
            count_False.append(all_variables[0] + '.' + str(i))
    all_word = ['Reachable', 'Unreachable']
    sh_ip_int_br = [(count_True, count_False)]
    print(tabulate(sh_ip_int_br, headers=all_word))


min_num = str(input('Введите начальный ip адресс (например: 192.0.0.1 , 10.0.5.5 , 7.8.8.8): '))
max_num = str(input('Введите конечный ip адресс (например: 192.0.0.100 , 10.0.5.95 , 7.8.8.78): '))

host_range_ping(min_num, max_num)
