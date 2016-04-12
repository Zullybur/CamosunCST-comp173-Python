# * * * * * * * * * * * * * * * * * * * * * * * #
# Server software to receive integers from      #
# client with operator and return calculation.  #
#                                               #
# Created by: Matthew Casiro                    #
# Created on: April 12 2016                     #
# * * * * * * * * * * * * * * * * * * * * * * * #

import socket

if __name__ == '__main__':
    port = 45678
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", port))

    # Wait for incoming connections and process data
    while true:
        inTuple = s.recvfrom()
        s.connect((inTuple[0], "Hello, {}".format(inTuple[1])))