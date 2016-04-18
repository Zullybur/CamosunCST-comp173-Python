# * * * * * * * * * * * * * * * * * * * * * * * #
# Server software to receive integers from      #
# client with operator and return calculation.  #
#                                               #
# Created by: Matthew Casiro                    #
# Creasted on: April 12 2016                    #
# * * * * * * * * * * * * * * * * * * * * * * * #

import socket
import sys

if __name__ == '__main__':
    TRANS_SIZE = 4096
    RESULT_SIZE = 4
    MASK_NIB = 2**4 - 1
    MASK_LSB = 2**8 - 1

    port = sys.argv[1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Wait for incoming connections and process data
    s.bind(("", int(port)))
    while True:
        data, address = s.recvfrom(TRANS_SIZE)
        # Initialize received data
        opcode = int(data[0])
        count = int(data[1])
        if count == 0:
            result = 0
        else:
            result = (int(data[2]) >> 4)
            for i in range(1, count):
                if i % 2 == 0:
                    if opcode == 2**0:
                        result += (int(data[i//2+2])) >> 4
                    if opcode == 2**1:
                        result -= (int(data[i//2+2])) >> 4
                    if opcode == 2**2:
                        result *= (int(data[i//2+2])) >> 4
                else:
                    if opcode == 2**0:
                        result += (int(data[i//2+2])) & MASK_NIB
                    if opcode == 2**1:
                        result -= (int(data[i//2+2])) & MASK_NIB
                    if opcode == 2**2:
                        result *= (int(data[i//2+2])) & MASK_NIB
        # Prepare result as byte array and submit to client
        b = bytearray(RESULT_SIZE)
        b[0] = (result >> 24) & MASK_LSB
        b[1] = (result >> 16) & MASK_LSB
        b[2] = (result >> 8) & MASK_LSB
        b[3] = result & MASK_LSB
        s.sendto(b, address)