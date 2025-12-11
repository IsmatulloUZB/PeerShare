import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ison = False

def changeserverstatus(status):
    global ison
    ison = status

def getfile(filename, filesize, client_socket1, cb_showrecievingfile):
    i = 0
    recieved = 0
    with open("received_" + filename, "wb") as f:
        while True:
            if i==0:
                i = 1
                cb_showrecievingfile("receiving: " + filename)
                sendmessage("<true>")
            bytes_read = client_socket1.recv(1024)
            if not bytes_read:
                break

            f.write(bytes_read)
            recieved += len(bytes_read)
#            print("RECEIVED: ", recieved)
            if recieved >= int(filesize):
                cb_showrecievingfile("received: " + filename)
                break



def serverstart(cb_name, cb_message, myname, port, cb_server_failed, cb_freezeentry, cb_sendfile):
    try:
        server.bind(('0.0.0.0', int(port)))
        changeserverstatus(True)
        cb_freezeentry()
        server.listen(1)
        global client_socket
        client_socket, address = server.accept()
        data = client_socket.recv(1024).decode("utf-8")
        cb_name(data)
#        print(data, ' ulandi\n')

        client_socket.send(myname.encode("utf-8"))
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if message[0:6] == "<text>":
                cb_message(message[6:])
            elif message.startswith("<file>"):
                end = 6 + message[6:].find(">")
                filesize = int(message[6:end])
                filename = message[end + 1:]
                getfile(filename, filesize, client_socket, cb_message)
            elif message[0:6] == "<true>":
                cb_sendfile()
    except Exception as e:
        cb_server_failed()



def sendmessage(message):
#    print('Me:', message)
    client_socket.send(message.encode('utf-8'))


def sendfile(path):
    # Отправка содержимого файла порциями
    with open(path, "rb") as f:
        while True:
            bytes_read = f.read(1024)  # читаем 1024 байта
            if not bytes_read:
                break
#            print("read: ", bytes_read)
            client_socket.sendall(bytes_read)  # отправляем клиенту



# Бесконечный чат
if __name__ == "__main__":

    # выдаем айпи для сервака
    server.bind(('127.0.0.1', 8080))

    # сколько типов одновременно могут подключиться к серваку
    server.listen(4)

    print('Server ishga tushdi\n')
    name = input('Ismingizni kiriting: ')

    #
    client_socket, address = server.accept()
    # Макс. символы 1024 кб и декодирование из utf-8
    data = client_socket.recv(1024).decode('utf-8')

    print(data, ' ulandi\n')
    # Отправка нашего никнейма
    client_socket.send(name.encode('utf-8'))

    while True:
        message = input('Me: ')

        # отправка только что введеннего письмо по utf-8
        client_socket.send(message.encode('utf-8'))

        # получение максимум 1024 кб инфы и декодирование из utf-8
        message = client_socket.recv(1024)
        message = message.decode('utf-8')

        # вывод в консоль
        print(data, ':', message)



