# * * * * * * * * * * * * * * * * * * * * * * #
# Client software to send integers to server  #
# with operator for calculation.              #
#                                             #
# Created by: Matthew Casiro                  #
# Created on: April 12 2016                   #
# * * * * * * * * * * * * * * * * * * * * * * #

import socket
import sys

if __name__ == '__main__':
    SERVER = "localhost"
    PORT = 45678
    NAME = bytes(sys.argv[1], 'utf-8')
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((SERVER, PORT))
    s.sendall(NAME)
    result = s.recv(4096)
    print (result.decode('utf-8'))