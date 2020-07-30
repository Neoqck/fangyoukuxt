import socket
from conf import setting


def get_client():
    client = socket.socket()
    client.connect((setting.ip, setting.port))
    return client







