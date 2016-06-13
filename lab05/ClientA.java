package comp173.lab5;

import java.lang.UnsupportedOperationException;

public class ClientA {
    private enum connType {
        UDP, TCP
    }
    private String host;
    private int port;
    private int operatorCode;
    private int[] values;;

    public static void main(String[] args) {

        // Process command line args
        parseCommandLineArguments(args);
        // Built byte array
        byte[] b = buildByteArray();
        // Connect to server
        // conn = serverConnect();
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
    
    /**
     * Extract information from command line arguments
     */
    private static void parseCommandLineArguments(String[] args) {
        for (int i = 0; i < args.length; i++) {
            System.out.println("args["+i+"]: "+args[i]);
        }
    }

    /**
     * Create a byte array using nibbles packed in to bytes,
     * based off the system arguments
     */
    private static byte[] buildByteArray() {
        // [0] - operator (+: 2^0) (-: 2^1) (*: 2^2)
        // [1] - count of following integers
        // [2] - integers passed as nibbles
        throw new UnsupportedOperationException();
    }

    /**
     * Establish server connection
     */
    private static void serverConnect() {
        throw new UnsupportedOperationException();
    }

    /**
     * Receive and confirm initial server connection.
     * Return true if server sends "READY", otherwise return false;
     */
    private static boolean connGetReady() {
        throw new UnsupportedOperationException();
    }

    /**
     * Send the byte array to the server
     */
    private static void connSendByteArray() {
        throw new UnsupportedOperationException();
    }

    /**
     * Receive the result array from the server
     */
    private static byte[] connReceiveData() {
        throw new UnsupportedOperationException();
    }

    /**
     * Unpack the result from the server and handle case
     */
    private static int unpackResult() {
        throw new UnsupportedOperationException();
    }
}