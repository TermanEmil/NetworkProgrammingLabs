#!/usr/bin/env python3

import socket
import json
import time
from utils import *
from service_registry import SERVICE_REGISTRY_PORT


class ServiceRegistryUtil:
    def __init__(self, port):
        self.port = port

    def register_server(self, address, port, nb_of_tries=1):
        msg_obj = {
            "type": "register",
            "port": port,
            "address": address
        }
        msg = json.dumps(msg_obj)

        for i in range(nb_of_tries):
            udp_broadcast_msg(self.port, SERVICE_REGISTRY_PORT, msg)

            if i != nb_of_tries - 1:
                time.sleep(1)

        print("Registration sent!")

    def get_registered_server(self, nb_of_tries=2):
        msg_obj = {
            "type": "get_server",
            "port": self.port
        }
        msg = json.dumps(msg_obj)

        for i in range(nb_of_tries):
            udp_broadcast_msg(self.port, SERVICE_REGISTRY_PORT, msg=msg)

        for i in range(nb_of_tries):
            data = udp_read_msg(self.port)
            data_dict = json.loads(data)

            print(data_dict)
            if 'server_registered' not in data_dict:
                continue

            if not data_dict['server_registered']:
                return None

            return data_dict

        return None
