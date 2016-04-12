# * * * * * * * * * * * * * * * * * * * * * * #
# Client software to send integers to server  #
# with operator for calculation.              #
#                                             #
# Created by: Matthew Casiro                  #
# Created on: April 12 2016                   #
# * * * * * * * * * * * * * * * * * * * * * * #

import socket

if __name__ == '__main__':
    server = "localhost"
    port = 45678
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((server, port))
    s.sendall("Matthew")