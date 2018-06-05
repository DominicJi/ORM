import socket
from  conf import settings

def client_conn():
    client=socket.socket()
    client.connect_ex(settings.server_address)
    return client