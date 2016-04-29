import sys, socket

verbose = "-v" in sys.argv
debuging = "-d" in sys.argv

def tcpReq(server, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
    if len(sys.argv) < 5 or len(sys.argv) > 7:
        print (cmdLineError)
        sys.exit()

    s = tcpReq(sys.argv[1], int(sys.argv[2]))
    response = s.recv(1024).decode("UTF-8")
    if debugging: print ("Server Connect Response:",response)
    # Determine process request from command line
    if sys.argv[3] == "PUT":
        print("client sending file <filename> (<NNN> bytes)")
    elif sys.argv[3] == "GET":
        print("client receiving file <filename> (<NNN> bytes)")
    elif sys.argv[3] == "DEL":
        print("client deleting file <filename>")
    else:
        print (cmdLineError)

    

# int.from_bytes(data, byteorder='big', signed=false)
# data.to_bytes(8, byteorder='big', signed=false)