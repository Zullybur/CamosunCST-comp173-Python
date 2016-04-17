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
        print("data:", data)
        # Initialize received data
        opcode = int(data[0])
        count = int(data[1])
        if count == 0:
            result = 0
        else:
            result = (int(data[2]) >> 4)
            print(result)
            for i in range(1, count):
                print("for loop. i:", i)
                if i % 2 == 0:
                    print("op on even")
                    if opcode == 2**0:
                        result += (int(data[i//2+2])) >> 4
                    if opcode == 2**1:
                        result -= (int(data[i//2+2])) >> 4
                    if opcode == 2**2:
                        result *= (int(data[i//2+2])) >> 4
                else:
                    print("op on odd")
                    if opcode == 2**0:
                        result += (int(data[i//2+2])) & MASK_NIB
                    if opcode == 2**1:
                        result -= (int(data[i//2+2])) & MASK_NIB
                    if opcode == 2**2:
                        result *= (int(data[i//2+2])) & MASK_NIB
                    
                print(result)
        # Prepare result as byte array and submit to client
        b = bytearray(RESULT_SIZE)
        b[0] = (result >> 24)
        b[1] = (result >> 16) & MASK_LSB
        b[2] = (result >> 8) & MASK_LSB
        b[3] = result & MASK_LSB
        print (b)
        s.sendto(b, address)