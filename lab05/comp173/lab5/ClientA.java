package comp173.lab5;

import java.lang.*;
import java.net.Socket;
import java.net.SocketAddress;
import java.io.*;

public class ClientA {
    public static final int OFFSET = 3;
    public static final int MAX_PARAM = 15;
    public static final int MAX_BUFF = 1024;

    private static int offest;
    private enum connType {
        UDP, TCP
    }
    private static String host;
    private static int port;
    private static int operatorCode;
    private static int[] values;


    public static void main(String[] args) {

        // Process command line args
        parseCommandLineArguments(args);

        // Built byte array
        byte[] b = buildByteArray();

        // Create Socket and BufferedOutputStream, then write byte array to output stream
        Socket sock;
        BufferedInputStream bin;
        BufferedOutputStream bout;
        byte[] data = new byte[MAX_BUFF];

        try {
            sock = new Socket(host, port);
            bin = new BufferedInputStream(sock.getInputStream());
            bout = new BufferedOutputStream(sock.getOutputStream());
            
            bin.read(data, 0, MAX_BUFF);
            bout.write(b, 0, b.length);
        } catch (IOException ex) {
            System.out.println(ex);
            return;
        }
        

        // Connect to server
        // sock.connect()

        // // Receive READY
        // if (connGetReady()) {
        //     // Send byte array:
        //     connSendByteArray();
        // }
        
        // // Receive result
        // byte[] data = connReceiveData();

        // // Unpack result
        // int result = unpackResult();

        // // Display result + newline
        // System.out.println(result);
    }
    
    /**
     * Extract information from command line arguments
     */
    private static void parseCommandLineArguments(String[] args) throws ArrayIndexOutOfBoundsException, IllegalArgumentException {

        if (args.length > 13) throw new ArrayIndexOutOfBoundsException("Too many command line arguments!");

        // Assign command line args to class variables
        host = args[0];
        port = Integer.parseInt(args[1]);
        char opChar = args[2].charAt(0);

        // Assign bit flag to operatorCode based on input
        switch (opChar) {
            case '+':
                operatorCode = (int)Math.pow(2, 0);
                break;
            case '-':
                operatorCode = (int)Math.pow(2, 1);
                break;
            case '*':
                operatorCode = (int)Math.pow(2, 2);
                break;
            default:
                throw new IllegalArgumentException("Operator supplied was invalid!");
        }

        // Assign parameters to array of values
        values = new int[args.length - OFFSET];
        for (int i = 0; i < args.length - OFFSET; i++) {
            int tmp;
            try {
                tmp = Integer.parseInt(args[i + OFFSET]);
            } catch (NumberFormatException ex) {
                throw new IllegalArgumentException(ex);
            }
            if (tmp <= MAX_PARAM) {
                values[i] = tmp;
            } else {
                throw new IllegalArgumentException("Parameters must be less than " + MAX_PARAM);
            }
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
        byte[] b = new byte[values.length + 2];

        b[0] = (byte)operatorCode;
        b[1] = (byte)values.length;

        for (int i = 0; i < values.length; i += 2) {
            b[i + 2] = (byte)(values[i] << 4);
            try {
                b[i + 2] = (byte)(b[i + 2] | values[i + 1]);
            } catch (ArrayIndexOutOfBoundsException ex) {
                // Crash prevention - catch odd number of arguments
            }
        }
        return b;
    }

    private static void setupServer(Socket sock, BufferedInputStream bin, BufferedOutputStream bout) throws IOException {
        sock = new Socket(host, port);
        bin = new BufferedInputStream(sock.getInputStream());
        bout = new BufferedOutputStream(sock.getOutputStream());
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