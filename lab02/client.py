import sys, socket

def tcpReq(server, port):
    s = socket.socket(socket.AF_INET, socket.STREAM)
    s.connect((server, port))
    return s

def getFile():
    pass

def putFile():
    pass

def delFile():
    pass

if __name__ == '__main__':
    cmdLineError = "Usage: client.py server_address port [PUT|GET|DEL] filename"
    if len(sys.argv) < 4:
        print (cmdLineError)
        return
    # Determine process request from command line
    if sys.argv[3] == "PUT":
        pass
    elif sys.argv[3] == "GET":
        pass
    elif sys.argv[3] == "DEL":
        pass
    else:
        print (cmdLineError)

    s = tcpReq(sys.argv[1], int(sys.argv[2]))