package comp173.lab5;

import java.lang.*;
import java.net.Socket;
import java.net.SocketAddress;
import java.io.*;

public class ClientB {
    public static final int OFFSET = 3;
    public static final int MAX_PARAM = 15;
    public static final int MAX_BUFF = 1024;
    public static final String READY_RESPONSE = "READY";
    public static final int READY_INDEX = 5;

    private static String host;
    private static int port, operatorCode;
    private static int[] values;

    private static Socket sock;
    private static BufferedReader bread;
    private static BufferedOutputStream bout;
    private static DataInputStream din;

    public static void main(String[] args) {
        // Process command line args
        parseCommandLineArguments(args);

        // Built byte array
        byte[] b = buildByteArray();

        try {
            // Set up socket with server
            setUpSocket();

            // Get and check READY response from server
            if (!connGetReady()) {
                System.out.println("Bad response from server");
                return;
            }
            // System.out.println("Sending data to server now");
            // Send data to server
            bout.write(b, 0, b.length);
            bout.flush();
            // System.out.println("Sent data to server now");

            // Receive result
            int result = din.readInt();
            System.out.println(result);

        } catch (IOException ex) {
            System.out.println(ex);
            return;
        }
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
        byte[] b = new byte[(values.length / 2) + (values.length % 2 == 0 ? 2 : 3)];
        // System.out.println("values.length: "+values.length);
        // System.out.println("b.length: "+b.length);

        b[0] = (byte)operatorCode;
        b[1] = (byte)values.length;

        for (int i = 0, j = 2; i < values.length; ) {
            b[j] = (byte)(i % 2 == 0 ? values[i++] << 4 : b[j++] | values[i++]);
        }
        return b;
    }

    private static void setUpSocket() throws IOException {
        try {
            sock = new Socket(host, port);
            bread = new BufferedReader(new InputStreamReader(sock.getInputStream()));
            bout = new BufferedOutputStream(sock.getOutputStream());
            din = new DataInputStream(sock.getInputStream());
        } catch (IOException ex) {
            throw new IOException(ex);
        }
    }
    /**
     * Receive and confirm initial server connection.
     * Return true if server sends "READY", otherwise return false;
     */
    private static boolean connGetReady() {
        try {
            // Wait for READY initiation from server
            // System.out.println("About to receive READY");
            char[] tmp = new char[5];
            bread.read(tmp, 0, tmp.length);
            String ready = new String(tmp);

            // System.out.println("Received: "+ ready);
            if (ready.equals(READY_RESPONSE)) {
                return true;
            }
            return false;
        } catch (IOException ex) {
            System.out.println(ex);
        }
        return false;
    }
}