import sys, socket

verbose = "-v" in sys.argv
debug = "-d" in sys.argv

# if verbose: print("")
# if debug: print("")

# 
def makeTCPConnection(address):
    if debug: print("Making connection")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(address)
    if debug: print("Connection made")
    return s
# 
def checkResponse(s, expected):
    response = s.recv(1024).decode("UTF-8")

    if response != expected:
        if verbose: print ("Server Error!", response)
        return False

    if verbose: print ("Server response:", response)
    return True

# Request a resource from a web server
# Pre: there is a TCP connection made with a webserver
# Post: the socket is receiving the resource to the buffer
# Param s: is a socket object
# Param uri: is a resource string to be requested from the web server, begining with "/"
def getHTML(s, uri):
    request = "GET "+uri+"\n\n"
    encodedRequest = request.encode("UTF-8")
    if debug: print("Making GET request")
    s.send(encodedRequest)

# Searches for 'term' in 'data' and truncates data 'beg'ining (before term) or 'end' (after term)
def cleanData(data, term, trunc):
    pos = data.upper().find(term.upper())
    if pos == -1:
        return False, data
    elif trunc == "beg":
        return True, data[pos:]
    elif trunc == "end":
        return True, data[:(pos + len(term))]

#
def sendData():
    pass

# Extract the program varaibles from the parameter
# Pre: N/A
# Post: N/A
# Param raw: a full web address begining with "http://"
def extractParams(raw):
    ignoredChars = 7
    i = raw.find("/", ignoredChars)
    host = raw[ignoredChars:i] if i > 0 else raw[ignoredChars:]
    resource = raw[i:] if i > 0 else "/"
    if verbose: print ("'extractParams' executed:\nraw: {}, i: {}, host: {}, resource: {}" .format(raw, i, host, resource))
    return host, resource

# Run main
if __name__ == '__main__':
    host, resource = extractParams(sys.argv[1])
    source = makeTCPConnection( (host, 80) )
    getHTML(source, resource)
    
    state = 1
    data = tmp = ""
    foundOpenHTML
    foundCloseHTML
    # Cycle states until all processes are finnished
    while state != 4:
        # Get data from web server until <HTML> is found
        if state == 1:
            tmp = source.recv(1024).decode("UTF-8")
            found, data = cleanData(data + tmp, "<html>", "beg")
            # Check for closing tag in same block and adjust state accordingly
            if found:
                found, data = cleanData(data, "</html>", "end")
                if found:
                    parser.send(data.encode("UTF-8"))
                    state = 3
                else:
                    state = 2
            else:
                data = tmp
            tmp = ""
        # Get data from source and send data to the parser, until </HTML> is found
        elif state == 2:
            tmp = source.recv(1024).decode("UTF-8")
            length = len(data)
            found, data = cleanData(data + tmp, "</html>", "end")
            if found:
                parser.send(data.encode("UTF-8"))
                state = 3
                tmp = data = ""
            else:
                parser.send(data[:length].encode("UTF-8"))
                data = tmp
        # Receive from parser until end of data flag is found
        elif state == 3:
            tmpparser.recv(1024).decode("UTF-8")
        # Catch any bad states
        else:
            state = 4

    # Pull data until the opening <HTML> tag is found
    proceed = False
    while not proceed:
        data = 
        proceed, cleaned = cleanData(data, "<HTML>", "beg")
        # if debug: print (cleaned)
    if verbose: print ("'<HTML>' found")
    
    # Check for matching closing tag in same data block
    oneblock, cleaned = cleanData(cleaned, "</HTML>", "end")
    if verbose and oneblock: print ("'</HTML>' found in first block")

    parser = makeTCPConnection( ("rtvm.cs.camosun.bc.ca", 10010) )
    if not checkResponse(parser, "READY"): sys.exit()
    if oneblock:
        if debug: print ("sending:", cleaned)
        parser.send(cleaned.encode("UTF-8"))
        data = parser.recv(1024).decode("UTF-8")
        print (data)
    else:
        proceed = False
        while not proceed:
            data = requestHTTPData(source)
            proceed, cleaned = cleanData(data)
            sendData(parser, cleaned)