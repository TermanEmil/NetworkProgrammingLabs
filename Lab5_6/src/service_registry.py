#!/usr/bin/env python3

import socket
import threading
import json


SERVICE_REGISTRY_PORT = 4000


class RegisterCmd(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)


class RegisterEntry:
    def __init__(self, addr, port):
        self.address = addr
        self.port = port


if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.bind(("", 4000))

    registered_chat_server = None

    while True:
        data, addr = server.recvfrom(1024)
        cmd = RegisterCmd(data.decode('utf-8'))

        if cmd.type == 'register':
            registered_chat_server = RegisterEntry(cmd.address, cmd.port)
            print("Registered server: {0}:{1}", (cmd.address, cmd.port))
        elif cmd.type == 'get_server':
            if registered_chat_server is None:
                msg_obj = {"server_registered": False}
            else:
                msg_obj = {
                    "server_registered": True,
                    "address": registered_chat_server.address,
                    "port": registered_chat_server.port
                }
            msg = json.dumps(msg_obj)
            server.sendto(bytes(msg, 'utf-8'), ('<broadcast>', cmd.port))
        else:
            print("Invalid msg")
