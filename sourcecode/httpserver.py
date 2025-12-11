from http.server import HTTPServer, SimpleHTTPRequestHandler

import threading
import os

server = None
thread = None

import sys
sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')

def startwebsharing(path, port):
    global server, thread

    os.chdir(path)

    host = "0.0.0.0"
    server = HTTPServer((host, port), SimpleHTTPRequestHandler)

    def run():
        server.serve_forever()

    thread = threading.Thread(target=run, daemon=True)
    thread.start()


def stopwebsharing():
    global server, thread
#    print("Stopping web sharing...")
    server.shutdown()
    server.server_close()
    server = None
    thread = None
#    print("Web sharing was stopped.")


# пример
if __name__ == '__main__':
    import time
    startwebsharing("D:\\code", 8080)
    print("server started...")
    time.sleep(10)
    stopwebsharing()
    print("server stopped...")

