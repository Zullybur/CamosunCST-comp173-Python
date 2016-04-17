import sys

if __name__ == '__main__':
    print(eval("2+2"))
    print(eval("{}{}{}" .format(sys.argv[1], sys.argv[2], sys.argv[3])))
    # x = int(sys.argv[1])
    # y = int(sys.argv[2])
    # print (x & y)
    # mask = 2**8 - 1
    # value = x & mask
    # print (value)
