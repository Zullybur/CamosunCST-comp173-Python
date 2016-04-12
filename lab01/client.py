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
    address = (sys.argv[1], int(sys.argv[2]))
    b = bytearray()
    i = 0

    for v in sys.argv:
        if (i > 2):
            b.append(int(sys.argv[i]))
        i+=1

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(address)
    s.sendall(b)
    result = s.recv(4096)
    print (int(result[0]))