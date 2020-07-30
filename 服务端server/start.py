from socket_server import tcp_server
import os
import sys

sys.path.append(os.path.dirname(__file__))

if __name__ == '__main__':
    tcp_server.run()




