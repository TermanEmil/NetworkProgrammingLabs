import threading
import socket


print_lock = threading.Lock()


def thread_safe_print(string):
    with print_lock:
        print (string)


def udp_broadcast_msg(sender_port, destination_port, msg):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("", sender_port))

    msg_bytes = bytes(msg, 'utf-8')

    server.sendto(msg_bytes, ('<broadcast>', destination_port))
    server.close()


def udp_read_msg(port):
    reader = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    reader.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    reader.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    reader.bind(("", port))

    data, addr = reader.recvfrom(1024)
    reader.close()
    return data.decode('utf-8')
