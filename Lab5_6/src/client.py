#!/usr/bin/env python3

import socket
import threading
from utils import *
from service_registry_util import ServiceRegistryUtil


class ChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.socket = None
        self.user_input_thread = None
        self.server_listen_thread = None

    def __del__(self):
        if self.user_input_thread:
            self.user_input_thread.join()

        if self.server_listen_thread:
            self.server_listen_thread.join()

        if self.socket:
            self.socket.close()

    def init_connection(self):
        print('Initiating connection')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        print('Connected')

    def start_communication(self):
        self.user_input_thread = threading.Thread(target=self.read_user_input)
        self.server_listen_thread = threading.Thread(target=self.listen_to_server)

        self.user_input_thread.start()
        self.server_listen_thread.start()

    def read_user_input(self):
        while True:
            user_input = input()
            self.socket.sendall(bytes(user_input, 'utf-8'))

    def listen_to_server(self):
        while True:
            data = self.socket.recv(1024)

            if data is None or len(data) == 0:
                break

            thread_safe_print(data.decode('utf-8'))


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65443        # The port used by the server


if __name__ == '__main__':
    serviceRegistryUtil = ServiceRegistryUtil(PORT)
    server = serviceRegistryUtil.get_registered_server()
    print('server:', server)

    chatClient = ChatClient(server['address'], server['port'])
    chatClient.init_connection()
    chatClient.start_communication()
