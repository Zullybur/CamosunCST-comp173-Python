# * * * * * * * * * * * * * * * * * * * * * * * #
# Server software to receive integers from      #
# client with operator and return calculation.  #
#                                               #
# Created by: Matthew Casiro                    #
# Created on: April 12 2016                     #
# * * * * * * * * * * * * * * * * * * * * * * * #

import socket
import sys

if __name__ == '__main__':
    TRANS_SIZE = 4096
    RESULT_SIZE = 4
    port = sys.argv[1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", int(port)))

    # Wait for incoming connections and process data
    while True:
        result = bytearray(RESULT_SIZE)
        inTuple = s.recvfrom(TRANS_SIZE)
        data = inTuple[0]
        intVal = int(data[0])
        print (intVal + 1)
        result[0] = intVal + 1
        print (result)
        s.sendto(result, inTuple[1])