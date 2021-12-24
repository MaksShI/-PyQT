import subprocess

PROCESS = []

while True:
    ACTION = input('Выберите действие: q - выход, s - запустить сервер и клиенты, x - закрыть все окна: ')
    if ACTION == 'q':
        break
    elif ACTION == 's':
        p = int(input('Введите кол-во комиандных строк: '))
        k = 0
        PROCESS.append(subprocess.Popen('python server.py', creationflags=subprocess.CREATE_NEW_CONSOLE))
        for i in range(0, p):
            k += 1
            PROCESS.append(subprocess.Popen(f'python client.py -n test{k}', creationflags=subprocess.CREATE_NEW_CONSOLE))

    elif ACTION == 'x':
        while PROCESS:
            VICTIM = PROCESS.pop()
            VICTIM.kill()
