import sys

verbose = "-v" in sys.argv

# 
def makeTCPConnection(address):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(address)
    checkResponse(s)
    return s
# 
def checkResponse(s):
    response = s.recv(1024).decode("UTF-8")
    if response != "READY":
        if verbose: print ("Server Error!", response)
        sys.exit(1)
    if verbose: print ("Server response:", response)
# 
def requestData():
    pass
# Searches for 'term' in 'data' and clears text before if 'position' = "head" or after if 'position' = "tail"
def cleanData(data, term, position):
    pos = data.upper.find(term)
    if pos == -1:
        return false, data
    elif position = "head":
        return true, data[pos:]
    elif position = "tail":
        return true, data[:(pos + len(term)]
#
def sendData():
    pass

if __name__ == '__main__':
    source = makeTCPConnection()
    # Pull data until the opening <HTML> tag is found
    proceed = False
    data = ""
    while not proceed:
        data += requestData(source)
        proceed, cleaned = cleanData(data, "<HTML>", "head")
        # Check for matching closing tag in same data block
        if proceed:
            oneblock, cleaned = cleanData(cleaned, "</HTML>", "tail")
    # Handle the remaining data in the initial parse
    parser = makeConnection(("rtvm.cs.camosun.bc.ca", 10010))
    if oneblock:
        pass
    else:
        proceed = False
        while not proceed:
            data = requestData(source)
            proceed, cleaned = cleanData(data)
            sendData(parser, cleaned)