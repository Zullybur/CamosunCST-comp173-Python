import os, sys, socket

verbose = "-v" in sys.argv
debuging = "-d" in sys.argv

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", int(sys.argv[1])))
s.listen(0)

while True:
    if verbose: print("server waiting on port",sys.argv[1])
    conn, address = s.accept()
    if verbose: print ("server connected to client at {}:{}" .format(address[0], address[1]))
    conn.sendto("READY".encode("UTF-8"), address)