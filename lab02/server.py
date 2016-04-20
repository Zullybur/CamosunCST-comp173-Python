import sys, socket

verbose = "-v" in sys.argv
debuging = "-d" in sys.argv

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", int(sys.argv[1])))
s.listen(0)

while True:
    conn, address = s.accept()
    if verbose: print ("Connected:")