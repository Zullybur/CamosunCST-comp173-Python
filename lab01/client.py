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
    TRANS_SIZE = 4096
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    address = (sys.argv[1], int(sys.argv[2]))
    b = bytearray()

    # Add operator code
    if sys.argv[3] == '+':
        b.append(2**0)
    elif sys.argv[3] == '-':
        b.append(2**1)
    elif sys.argv[3] == '*':
        b.append(2**2)
    else:
        b.append(0)
    # Check paramater list count
    if len(sys.argv) > 15:
        maxRange = 15
    else:
        maxRange = len(sys.argv)
    b.append(maxRange - 4)
    # Add parameters
    for i in range(4, maxRange):
        if i % 2 == 0:
            b.append((int(sys.argv[i])) << 4)
        else:
            b[(i-3)//2] = b[(i-3)//2] | int(sys.argv[i])
    print(i)
    # Avoid multiplying by zero with an odd number of parameters
    if sys.argv[3] == '*' and i % 2 == 0:
        b[(i-4)//2] += 1
    print (b)
    # Connect to server, send data, and receive response
    s.connect(address)
    s.sendall(b)
    data = s.recv(TRANS_SIZE)
    print(data)
    # Process and output result
    result = ((int(data[0])) << 24) | ((int(data[1])) << 16) | ((int(data[2])) << 8) | (int(data[3]))
    print (result)
