package comp173.lab5;

public class ClientA {
    private enum connType {
        UDP, TCP
    }
    private String host;
    private int port;
    private int operatorCode;
    private int[] values;;

    /**
     * Extract information from command line arguments
     */
    private void parseCommandLineArguments(String[] args) {
        throw new NotImplementedException();
    }

    /**
     * Create a byte array using nibbles packed in to bytes,
     * based off the system arguments
     */
    private byte[] buildByteArray() {
        // [0] - operator (+: 2^0) (-: 2^1) (*: 2^2)
        // [1] - count of following integers
        // [2] - integers passed as nibbles
        throw new NotImplementedException();
    }

    /**
     * Establish server connection
     */
    private something serverConnect() {
        throw new NotImplementedException();
    }

    /**
     * Receive and confirm initial server connection.
     * Return true if server sends "READY", otherwise return false;
     */
    private boolean connGetReady() {
        throw new NotImplementedException();
    }

    /**
     * Send the byte array to the server
     */
    private void connSendByteArray() {
        throw new NotImplementedException();
    }

    /**
     * Receive the result array from the server
     */
    private byte[] connReceiveData() {
        throw new NotImplementedException();
    }

    /**
     * Unpack the result from the server and handle case
     */
    private int unpackResult() {
        throw new NotImplementedException();
    }

    public static void main(String[] args) {

        // Process command line args
        parseCommandLineArguments(args);
        // Built byte array
        byte[] b = buildByteArray();
        // Connect to server
        conn = serverConnect();
        // Receive READY
        if (connGetReady()) {
            // Send byte array:
            connSendByteArray();
        }
        
        // Receive result
        byte[] data = connReceiveData();

        // Unpack result
        int result = unpackResult();

        // Display result + newline
        System.out.println(result);
    }
}