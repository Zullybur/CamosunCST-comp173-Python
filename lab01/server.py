# * * * * * * * * * * * * * * * * * * * * * * * #
# Server software to receive integers from      #
# client with operator and return calculation.  #
#                                               #
# Created by: Matthew Casiro                    #
# Created on: April 12 2016                     #
# * * * * * * * * * * * * * * * * * * * * * * * #

import socket

if __name__ == '__main__':
    PORT = 45678
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.bind(("", PORT))

    # Wait for incoming connections and process data
    while True:
        inTuple = s.recvfrom(4096)
        string = "Hello, {}" .format(inTuple[0].decode('utf-8'))
        s.sendto(bytes(string, 'utf-8'), inTuple[1])