package comp173.lab5;

public class ServerA {
    private enum connType {
        UDP, TCP
    }
    
    /**
     * Send the initial message to a client when ready to begin communication
     */
    private void initiateProtocol() {
        throw new NotImplementedException();
    }

    /**
     * Receive the data for calculation request from the client
     */
    private void receiveRequest() {
        throw new NotImplementedException();
    }

    /**
     * Close the connection
     */
    public static void main(String[] args) {
        // Process command line args

        // PROTOCOL:
        //     -- Send READY on connect
        //     -- Receive Request
        //     -- Send Result
        //     -- Close Connection

    }
}