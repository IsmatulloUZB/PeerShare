import socket

def getfile(filename, filesize, client_socket, cb_showrecievingfile):
    i = 0
    recieved = 0
    with open("received_" + filename, "wb") as f:
        while True:
            if i==0:
                i = 1
                cb_showrecievingfile("receiving: " + filename)
                sendmessage("<true>")
            bytes_read = client_socket.recv(1024)
            if not bytes_read:
                break

            f.write(bytes_read)
            recieved += len(bytes_read)
#            print("RECEIVED: ", recieved)
            if recieved >= int(filesize):
                cb_showrecievingfile("received: " + filename)
                break

def connect(cb_name, cb_message, myname, cb_connection_lost, ip, port, cb_entry_freeze, cb_sendfile):
    try:
        global socket_server
        socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        print("connecting...")
        socket_server.connect((ip, int(port)))
#        print("connected")
        socket_server.send(myname.encode('utf-8'))
        socket_name = socket_server.recv(1024).decode('utf-8')
        cb_entry_freeze()
        cb_name(socket_name)
        while True:
            message = socket_server.recv(1024).decode('utf-8')
            if message[0:6] == "<text>":
                cb_message(message[6:])
            elif message.startswith("<file>"):
                end = 6 + message[6:].find(">")
                filesize = int(message[6:end])
                filename = message[end + 1:]
                getfile(filename, filesize, socket_server, cb_message)
            elif message[0:6] == "<true>":
                cb_sendfile()

    except ConnectionRefusedError:
#        print("Connection refused")
        cb_connection_lost()
    except OSError:
#        print("Connection refused Os error")
        cb_connection_lost()
    except ValueError:
#        print("Connection refused ValueError")
        cb_connection_lost()

def sendmessage(message):
#    print('Me:', message)
    socket_server.send(message.encode('utf-8'))

def sendfile(path):
    # Отправка содержимого файла порциями
    with open(path, "rb") as f:
        while True:
            bytes_read = f.read(1024)  # читаем 1024 байта
            if not bytes_read:
                break
#            print("read: ", bytes_read)
            socket_server.sendall(bytes_read)  # отправляем клиенту


if __name__ == '__main__':
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    name = input('Ismingizni kiriting: ')

    # Подключение к серваку
    socket_server.connect(('127.0.0.1', 8080))

    # Отправка никнейма
    socket_server.send(name.encode('utf-8'))

    # Получение ник от сервака
    socket_name = socket_server.recv(1024).decode('utf-8')
    print(socket_name, ':', ' ulandi')

    # socket_server.send(name.encode('utf-8')) - так пишется отправка данных
    # socket_name = socket_server.recv(1024).decode('utf-8') - а так пишется получение

    while True:
        message = socket_server.recv(1024).decode('utf-8')
        print(socket_name, ':', message)
        message = input('Me: ')
        socket_server.send(message.encode('utf-8'))
        message = input('Me: ')
        socket_server.send(message.encode('utf-8'))

