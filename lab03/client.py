def makeConnection():
    pass
def requestData():
    pass
def cleanData():
    pass
def sendData():
    pass

if __name__ == '__main__':
    source = makeConnection()
    # Pull data until the opening <HTML> tag is found
    proceed = False
    while not proceed:
        data = requestData(source)
        proceed, cleaned = cleanData(data)

    parser = makeConnection()
    sendData(parser, cleaned)

    proceed = False
    while not proceed:
        data = requestData(source)
        proceed, cleaned = cleanData(data)
        sendData(parser, cleaned)