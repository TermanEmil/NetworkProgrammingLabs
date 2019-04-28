#!/usr/bin/env python3

import socket
import threading
from utils import *
from service_registry_util import ServiceRegistryUtil


class Client:
    def __init__(self, address, connection):
        self.address = address
        self.connection = connection
        self.thread = None

    def __del__(self):
        self.connection.close()


class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.broadcast_lock = threading.Lock()

        self.socket = None
        self.connection_listener = None

    def __del__(self):
        if self.socket:
            self.socket.close()

        if self.connection_listener:
            self.connection_listener.join()

    def init_connection(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))

    def start_accepting_next_connections(self):
        self.connection_listener = threading.Thread(target=self.accept_new_connections)
        self.connection_listener.start()

    def accept_new_connections(self):
        while True:
            self.socket.listen()
            conn, addr = self.socket.accept()
            client = Client(address=addr, connection=conn)
            client.thread = threading.Thread(target=lambda: self.listen_to_client(client))
            client.thread.start()

            self.clients.append(client)
            thread_safe_print(str.format("New connection: {0}", addr))

    def listen_to_client(self, client):
        while True:
            try:
                data = client.connection.recv(1024)
            except:
                break

            if not data:
                client.connection.close()
                self.clients.remove(client)

            self.broadcast_msg(client, data)

    def broadcast_msg(self, sender, data):
        isinstance(sender, Client)

        with self.broadcast_lock:
            msg = "{0}: {1}".format(sender.address, data.decode('utf-8'))
            thread_safe_print(msg)

            msg_bytes = bytes(msg, 'utf-8')
            for client in self.clients:
                client.connection.sendall(msg_bytes)


HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65420        # Port to listen on (non-privileged ports are > 1023)


if __name__ == '__main__':
    serviceRegisterUtil = ServiceRegistryUtil(PORT)
    serviceRegisterUtil.register_server(port=PORT, address=HOST, nb_of_tries=2)

    server = ChatServer(host=HOST, port=PORT)
    server.init_connection()
    server.start_accepting_next_connections()
