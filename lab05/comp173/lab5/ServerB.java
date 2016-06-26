package comp173.lab5;

import java.lang.*;
import java.net.*;
import java.io.*;

public class ServerB {
    public static final int MAX_BUF = 1024;

    // Cmd line arg flags
    private static boolean verbose, debugging;

    // Networking objects
    private static Socket clientSock;
    private static PrintWriter pwrite;
    private static BufferedInputStream bin;
    private static DataOutputStream dout;

    // Class Variables
    private static byte[] data = new byte[MAX_BUF];
    
    public static void main(String[] args) {
        setFlags(args);

        // Process command line args
        int port = Integer.parseInt(args[0]);

        // Set up server connection
        ServerSocket serverSock;

        try {
            serverSock = new ServerSocket(port);
        } catch (IOException ex) {
            System.out.println(ex);
            return;
        }

        while(true) {
            try {
                // Set up client connection
                clientSock = serverSock.accept();
                pwrite = new PrintWriter(clientSock.getOutputStream());
                bin = new BufferedInputStream(clientSock.getInputStream());
                dout = new DataOutputStream(clientSock.getOutputStream());

                // Send READY and get response
                if (verbose) System.out.println(
                    "Connection made, sending ready and receiving results.");
                sendReadyGetResponse();

                int numParams = data[1];

                if (numParams <= 0) {
                    if (verbose) System.out.println("No data received.");
                    continue;
                }

                int[] params = getParams(numParams);

                if (debugging) {
                    System.out.println("Parsed Data:");
                    int i;
                    for (i = 0; i < numParams - 1; i++) {
                        System.out.print(params[i] + ", ");
                    }
                    System.out.println(params[i]);
                }

                // Complete operation on parameters
                int result = calculate(data[0], params);

                if (debugging) {
                    System.out.println("Result: " + result);
                }

                // Send back result and close connection
                dout.writeInt(result);
                dout.flush();
                clientSock.close();
            } catch (IOException ex) {
                System.out.println("ERROR!\n"+ex);
            }
        }
    }

    /**
     * Calculate the result of the given operation on the gifen paramenters
     */
    private static int calculate(int op, int[] params) throws IllegalArgumentException {
        int result = params[0];
        for (int i = 1; i < params.length; i++) {
            switch (op) {
                case 1:
                    result += params[i];
                    break;
                case 2:
                    result -= params[i];
                    break;
                case 4:
                    result *= params[i];
                    break;
                default:
                    System.out.println("Operator definition error.");
                    throw new IllegalArgumentException();
            }
        }
        return result;
    }

    /**
     * Extract parameters for calculation from byte array
     */
    private static int[] getParams(int num) {
        int[] params = new int[num];
        for (int i = 0, j = 2; i < num; ) {
            params[i++] = (data[j] >> 4) & (int)(Math.pow(2,4) - 1);
            if (num % 2 == 0 || i < num) {
                params[i++] = data[j++] & (int)(Math.pow(2,4) - 1);
            }
        }
        return params;
    }

    /**
     * Send "READY" to client to initiate data transfer, and receive the data
     */
    private static void sendReadyGetResponse() {
        try {
            pwrite.print("READY");
            pwrite.flush();
            if (verbose) System.out.println("READY sent");
            if (pwrite.checkError()) {
                System.out.println("Error occured in print writer");
            }
            bin.read(data, 0, 1024);
            if (verbose) System.out.println("Received array of size: " + data.length);
        } catch (IOException ex) {
            System.out.println(ex);
        }
    }

    /**
     * Check through command line arguments for flags
     */
    private static void setFlags(String[] args) {
        for (String arg : args) {
            if (arg.equals("-v"))
                verbose = true;
            if (arg.equals("-d"))
                debugging = true;
        }
    }
}