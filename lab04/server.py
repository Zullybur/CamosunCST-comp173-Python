import os, sys, socket, threading, queue

verbose = "-v" in sys.argv
debugging = "-d" in sys.argv

class Manager(threading.Thread):
    # Constructor
    def __init__(self, maxSize):
        threading.Thread.__init__(self)
        self.maxSize = maxSize
        self.running = set()
        self.q = queue.Queue

    # Add elements to queue
    def add(newT):
        newT.start()
        running.add(newT)

    # Check running set and add/remove as appropriate
    def run(self):
        while (True):
            # Remove dead threads
            for thread in running:
                if not thread.isAlive():
                    running.remove(thread)
            if running
            # Check for new threads waiting
            if len(q) < 1:
                sleep(1)
                continue
            else:
                if len(running) >= maxSize:
                    sleep(1)
                    continue
                else:
                    self.add(q.get())

# Thread handler to send, receive or delete files
class ClientHandler(threading.Thread):
    # Constructor
    def __init__(self, tid, conn, cmd):
        threading.Thread.__init__(self)

        self.tid = tid
        self.conn = conn
        this.cmd = cmd

    # Output thread state
    def toString(self):
        print("toString not implemented yet")

    # Initialize code
    def run(self):
        if self.cmd == "PUT":
            if debugging: print("command is PUT (takeFile)")
            takeFile(conn, filePath)
        elif self.cmd == "GET":
            if debugging: print("command is GET (giveFile)")
            giveFile(conn, filePath)
        elif self.cmd == "DEL":
            if debugging: print("command is DEL (delFile)")
            delFile(conn, filePath)
        else:
            print ("Wait how did I get here? (sanity check failed)")
        if verbose: print("closing connection")
        conn.close()

    # Receive and pars incoming command
    def tcpRecvCommand(conn):
        data = conn.recv(1024).decode("UTF-8")
        if verbose: print("server receiving request:", data)

        # return command and filePath from format: "CMD filePath"
        dataArray = data.strip().split(" ")
        return dataArray[0].strip(), dataArray[1].strip()

    # Process a "GET" command
    def giveFile(conn, filePath):
        if not os.access(filePath, os.R_OK) or not os.path.isfile(filePath):
            failResponse(conn, "{} does not exist" .format(filePath))
            return
        continueResponse(conn)
        response = conn.recv(1024)

        # Verify client response
        if (response.decode("UTF-8"))[0:5] != "READY": return
        size = os.path.getsize(filePath)
        if debugging: print ("Sending # of bytes:", size)
        conn.send(size.to_bytes(8, byteorder='big', signed=False))
        response = conn.recv(1024).decode("UTF-8")
        if response != "OK": return
        readFile(conn, filePath, size)
        conn.send("DONE".encode("UTF-8"))

    def readFile(conn, filePath, size):
        with open(filePath, 'rb') as f:
            while size > 0:
                data = f.read(min(size, 1024))
                conn.send(data)
                size -= len(data)

    # Process a "PUT" command
    def takeFile(conn, filePath):
        # Verify access to filepath
        if not os.access(".", os.R_OK):
            failResponse(conn, "unable to create file {}" .format(filePath))
            return

        # Request next recv to get file size
        continueResponse(conn)
        size = int.from_bytes(conn.recv(8), byteorder='big', signed=False)
        if debugging: print ("Client says size:", size)
        continueResponse(conn)
        writeFile(conn, filePath, size)
        if not os.path.isfile(filePath):
            failResponse(conn, "unable to create file {}" .format(filePath))
        else:
            successResponse(conn)

    # Write a file passed over a server connection    
    def writeFile(conn, filePath, size):
        with open(filePath, 'wb') as f:
            while size > 0:
                data = conn.recv(1024)
                f.write(data)
                size -= len(data)

    # Process a "DEL" command
    def delFile(conn, filePath):
        if os.path.exists(filePath): 
            if verbose: print("server deleting file", filePath)
            os.remove(filePath)
            if os.path.exists(filePath):
                failResponse(conn, "unable to delete {}" .format(filePath))
            else:
                successResponse(conn)
        else:
            if debugging: print("requested file {} not found" .format(filePath))
            failResponse(conn, "{} does not exist" .format(filePath))

    # Send response to indicate ready for next data chunk
    def continueResponse(conn):
        conn.send("OK".encode("UTF-8"))

    # Send response to indicate task complete and connection closing
    def successResponse(conn):
        conn.send("DONE".encode("UTF-8"))

    # Send an error response to the client
    def failResponse(conn, err):
        conn.send(("ERROR: {}" .format(err)).encode("UTF-8"))

# Open a tcp connection listener
def tcpListen(address, queue):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(address)
    s.listen(queue)
    return s

# Accept an incoming connection
def tcpAccept(s):
    if verbose: print("server waiting on port",sys.argv[1])
    conn, address = s.accept()
    if verbose: print ("server connected to client at {}:{}" .format(address[0], address[1]))
    return conn

# Accept incoming tcp connections and process commands
if __name__ == '__main__':
    address = ("", int(sys.argv[1]))
    maxThreads = int(sys.argv[2])
    s = tcpListen(address, 0)
    while True:
        conn = tcpAccept(s)
        command, filePath = tcpRecvCommand(conn)
        # Determine command and execute instruction
        