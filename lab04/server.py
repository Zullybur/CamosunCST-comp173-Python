import os, sys, socket, threading, queue, time

verbose = "-v" in sys.argv
debugging = "-d" in sys.argv

class Manager(threading.Thread):
    # Constructor
    def __init__(self, maxSize):
        threading.Thread.__init__(self)
        self.maxSize = maxSize
        self.running = set()
        self.q = queue.Queue()

    # Add elements to queue
    def enqueue(self, newT):
        self.q.put(newT)

    # Add elements to the running set
    def add(self, queuedT):
        self.running.add(queuedT)
        queuedT.start()

    # Remove dead threads
    def removeDeadThreads(self):
        for thread in self.running:
            if not thread.isAlive():
                self.running.remove(thread)
                break

    # Check running set and add/remove as appropriate
    def run(self):
        while (True):
            self.removeDeadThreads()
            # Sleep and loop if no threads waiting
            if self.q.empty():
                time.sleep(1)
            # Add a thread if space is available, otherwise sleep and loop
            else:
                if len(self.running) < self.maxSize:
                    self.add(self.q.get())
                else:
                    time.sleep(1)

# Thread handler to send, receive or delete files
class ClientHandler(threading.Thread):
    # Constructor
    def __init__(self, tid, conn):
        threading.Thread.__init__(self)
        self.tid = tid
        self.conn = conn
        if debugging: print("Thread {} initialized with:\n\tConnection: {}" .format(self.tid, self.conn,))

    # Output thread state
    def toString(self):
        print("toString not implemented yet")

    # Receive and pars incoming command
    def tcpRecvCommand(self, conn):
        data = conn.recv(1024).decode("UTF-8")
        if verbose: print("server receiving request:", data)

        # return command and filePath from format: "CMD filePath"
        dataArray = data.strip().split(" ")
        return dataArray[0].strip(), dataArray[1].strip()

    # Process a "GET" command
    def giveFile(self, conn, filePath):
        if not os.access(filePath, os.R_OK) or not os.path.isfile(filePath):
            self.failResponse(conn, "{} does not exist" .format(filePath))
            return
        self.continueResponse(conn)
        response = conn.recv(1024)

        # Verify client response
        if (response.decode("UTF-8"))[0:5] != "READY": return
        size = os.path.getsize(filePath)
        if debugging: print ("Sending # of bytes:", size)
        conn.send(size.to_bytes(8, byteorder='big', signed=False))
        response = conn.recv(1024).decode("UTF-8")
        if response != "OK": return
        self.readFile(conn, filePath, size)
        conn.send("DONE".encode("UTF-8"))

    def readFile(self, conn, filePath, size):
        with open(filePath, 'rb') as f:
            while size > 0:
                data = f.read(min(size, 1024))
                conn.send(data)
                size -= len(data)

    # Process a "PUT" command
    def takeFile(self, conn, filePath):
        # Verify access to filepath
        if not os.access(".", os.R_OK):
            self.failResponse(conn, "unable to create file {}" .format(filePath))
            return

        # Request next recv to get file size
        self.continueResponse(conn)
        size = int.from_bytes(conn.recv(8), byteorder='big', signed=False)
        if debugging: print ("Client says size:", size)
        self.continueResponse(conn)
        self.writeFile(conn, filePath, size)
        if not os.path.isfile(filePath):
            self.failResponse(conn, "unable to create file {}" .format(filePath))
        else:
            self.successResponse(conn)

    # Write a file passed over a server connection    
    def writeFile(self, conn, filePath, size):
        with open(filePath, 'wb') as f:
            while size > 0:
                data = conn.recv(1024)
                f.write(data)
                size -= len(data)

    # Process a "DEL" command
    def delFile(self, conn, filePath):
        if os.path.exists(filePath): 
            if verbose: print("server deleting file", filePath)
            os.remove(filePath)
            if os.path.exists(filePath):
                self.failResponse(conn, "unable to delete {}" .format(filePath))
            else:
                self.successResponse(conn)
        else:
            if debugging: print("requested file {} not found" .format(filePath))
            self.failResponse(conn, "{} does not exist" .format(filePath))

    # Send response to indicate ready for next data chunk
    def continueResponse(self, conn):
        conn.send("OK".encode("UTF-8"))

    # Send response to indicate task complete and connection closing
    def successResponse(self, conn):
        conn.send("DONE".encode("UTF-8"))

    # Send an error response to the client
    def failResponse(self, conn, err):
        conn.send(("ERROR: {}" .format(err)).encode("UTF-8"))

    # Initialize code
    def run(self):
        if debugging: print("Thread {} started." .format(self.tid))

        self.conn.send("READY".encode("UTF-8"))
        cmd, filePath = self.tcpRecvCommand(self.conn)

        if cmd == "PUT":
            if debugging: print("command is PUT (takeFile)")
            self.takeFile(self.conn, filePath)
        elif cmd == "GET":
            if debugging: print("command is GET (giveFile)")
            self.giveFile(self.conn, filePath)
        elif cmd == "DEL":
            if debugging: print("command is DEL (delFile)")
            self.delFile(self.conn, filePath)
        else:
            print ("Wait how did I get here? (sanity check failed)")
        if verbose: print("closing connection")
        self.conn.close()

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
    mgr = Manager(maxThreads)
    mgr.start()
    s = tcpListen(address, 0)
    i = 0
    while True:
        conn = tcpAccept(s)
        i += 1
        thread = ClientHandler(i, conn)
        mgr.enqueue(thread)