import sys, socket, os

debugging = "-d" in sys.argv

def tcpReq(server, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server, port))
    if debugging: print ("Making connection on:", address, port)
    response = s.recv(1024).decode("UTF-8")
    if debugging: print ("Server says:", response)
    if response == "READY":
        return s
    else:
        printError(response)
# Sample usage: client.py localhost 12345 GET test.txt
def getFile(command, filePath):
    # Make connection and send command
    s = tcpReq(address, port)
    command += " " + filePath
    s.send(command.encode("UTF-8"))
    if debugging: print ("Sending command:", command)
    response = s.recv(1024)
    # Verify server response
    if (response.decode("UTF-8"))[0:5] == "ERROR":
        printError(response.decode("UTF-8"))
    s.send("READY".encode("UTF-8"))
    # Receive number of bytes from server
    response = s.recv(8)
    size = int.from_bytes(response, byteorder='big', signed=False)
    if debugging: print ("Server says size:", size)
    # Send OK to server
    if debugging: print ("Sending \"OK\"")
    s.send("OK".encode("UTF-8"))
    # Write file to disk
    print ("client receiving file {} ({} bytes)" .format(filePath, size))
    with open(filePath, 'wb') as f:
        while size > 0:
            data = s.recv(min(size, 1024))
            f.write(data)
            size -= len(data)
    if debugging: print ("Done reading file")
    # Check for DONE
    response = s.recv(4).decode("UTF-8")
    if response == "DONE":
        print("Complete")
    else:
        printError(response)
# Sample usage: client.py localhost 12345 PUT test.txt
def putFile(command, filePath):
    # Verify existence and access to file
    if not os.access(filePath, os.R_OK) or not os.path.isfile(filePath):
        print("No access to file: " + filePath)
        sys.exit(1)
    # Make connection and send command
    s = tcpReq(address, port)
    command += " " + filePath
    s.send(command.encode("UTF-8"))
    if debugging: print ("Sending command:", command)
    response = s.recv(1024).decode("UTF-8")
    if debugging: print ("Server says:", response)
    # Verify server response
    if response != "OK":
        printError(response)
    # Get and send filesize to server
    size = os.path.getsize(filePath)
    if debugging: print ("Sending # of bytes:", size)
    s.send(size.to_bytes(8, byteorder='big', signed=False))
    response = s.recv(1024).decode("UTF-8")
    if debugging: print ("Server says:", response)
    # Verify server response
    if response != "OK":
        printError(response)
    print("client sending file {} ({} bytes)" .format(filePath, size))
    # Send data in chunks of 1024 bytes
    with open(filePath, 'rb') as f:
        while size > 0:
            data = f.read(1024)
            s.send(data)
            size -= len(data)
    response = s.recv(1024).decode("UTF-8")
    if debugging: print("Server says:", response)
    # Verify server response
    if response == "DONE":
        print("Complete")
    else:
        printError(response)
# Sample usage: client.py localhost 12345 DEL test.txt
def delFile(command, filePath):
    # Make connection and send command
    s = tcpReq(address, port)
    command += " " + filePath
    s.send(command.encode("UTF-8"))
    if debugging: print ("Sending command:", command)
    print("client deleting file", filePath)
    response = s.recv(1024).decode("UTF-8")
    if response == "DONE":
        print ("Complete")
    else:
        printError(response)
# Print error messages from the server
def printError(err):
    print("Server returned error:", err[7:])
    sys.exit(1)

if __name__ == '__main__':    
    cmdLineError = "Usage: client.py server_address port [PUT|GET|DEL] filename"
    # Verify srgv size is within expected range
    if len(sys.argv) < 5 or len(sys.argv) > 7:
        print (cmdLineError)
        sys.exit()
    # Pull arguments from command line
    address = sys.argv[1]
    port = int(sys.argv[2])
    command = sys.argv[3]
    filePath = sys.argv[4]

    # Execute process requested
    if command == "PUT":
        putFile(command, filePath)
    elif command == "GET":
        getFile(command, filePath)
    elif command == "DEL":
        delFile(command, filePath)
    else:
        print (cmdLineError)