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
    if verbose: print ("cleanData.find returned:", pos)
    endPt = pos + len(term)
    if pos == -1:
        return False, data
    elif trunc == "beg":
        if debug: print ("5 char test data[{}:5]:{}" .format(pos, data[pos:5]))
        return True, data[pos:]
    elif trunc == "end":
        if endPt == len(data):
            return True, data
        else:
            return True, data[:endPt]

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
    oldData = newData = ""
    parseEnd = "COMP173 HTML CONVERT COMPLETE"

    # Cycle states until all processes are finnished
    while state != 4:
        # Get data from web server until <HTML> is found
        if state == 1:
            tmp = source.recv(1024).decode("UTF-8")
            found, data = cleanData(data + tmp, "<html>", "beg")
            if debug: print("Cleaned data:\n{}\nEND" .format(data))
            # Check for closing tag in same block and adjust state accordingly
            if found:
                if verbose: print ("found <html>")
                parser = makeTCPConnection( ("rtvm.cs.camosun.bc.ca", 10010) )
                if not checkResponse(parser, "READY"): sys.exit(1)
                found, data = cleanData(data, "</html>", "end")
                if debug: print("Re-Cleaned data:\n{}\nEND" .format(data))
                if found:
                    if verbose: print ("found </html> in same block")
                    parser.send(data.encode("UTF-8"))
                    if debug: print ("Sending:\n{}\nEND SEND" .format(data))
                    state = 3
                    data = tmp = ""
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
            if debug: print("Cleaned data:\n", data, "\nEND")
            if found:
                if verbose: print ("found </html>")
                parser.send(data.encode("UTF-8"))
                state = 3
                tmp = data = ""
            else:
                parser.send(data[:length].encode("UTF-8"))
                data = tmp
        # Receive from parser until end of data flag is found
        elif state == 3:
            length = len(oldData)
            newData = parser.recv(1024).decode("UTF-8")
            found, combined = cleanData(oldData + newData, parseEnd, "end")
            if debug: print("Cleaned data from parser:\n" + combined +"\nEND CLEANED")
            if found:
                print (combined[:len(combined) - len(parseEnd)], end="", flush=True)
                state = 4
            else:
                print (oldData, end="", flush=True)
                oldData = newData
            # if debug: print ("State 3 start: newData[{}], data[{}], found[{}]" .format(newData, data, found))
            # found, data = cleanData(oldData + newData, parseEnd, "end")
            # if found:
            #     if debug: print("SLICING: {} by [{}:{}]" .format(len(data), length, len(data) - len(parseEnd)))
            #     print(data[length:(len(data) - len(parseEnd))], end="", flush=True)
            #     state = 4
            # else:
            #     print(newData, end="", flush=True)
            #     oldData = newData
            #     newData = ""

        # Catch any bad states
        else:
            parser.send("OK").encode("UTF-8")
            state = 4