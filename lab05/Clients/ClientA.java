package lab5;

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
     * Create a byte array using nibbles packed in to bytes
     */
    private void buildByteArray() {
        throw new NotImplementedException();
    }

    /**
     * Establish server connection
     */
    private static something serverConnect() {
        throw new NotImplementedException();
    }


    public static void main(String[] args) {

        // Process command line args
        parseCommandLineArguments(args);
        // Built byte array
        buildByteArray();
        // Connect to server
        conn = serverConnect();
        // Receive READY
        if (connGetReady()) {
            connSendByteArray();
        }
        /*
         * Send byte array:
         * [0] - operator (+: 2^0) (-: 2^1) (*: 2^2)
         * [1] - count of following integers
         * [2] - integers passed as nibbles
         */
g
        // Receive result
        connReceiveData();
        // Unpack result
        int result = unpackNibbles();
        // Display result + newline
        System.out.println(result);
    }
}