package comp173.lab5;

import java.lang.*;
import java.net.*;
import java.io.*;

public class ServerA {
    public static final int MAX_BUF = 1024;
    public static final int MAX_INT = 4;

    private static boolean verbose, debugging;

    private static Socket clientSock;
    private static BufferedInputStream bin;
    private static BufferedOutputStream bout;
    private static byte[] data = new byte[MAX_BUF];
    private static byte[] bArray = new byte[MAX_INT];
    
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
                clientSock = serverSock.accept();
                bin = new BufferedInputStream(clientSock.getInputStream());
                bout = new BufferedOutputStream(clientSock.getOutputStream());

                if (verbose) System.out.println("Connection made, sending ready and receiving results.");
                sendReadyGetResponse();

                // If debugging, print out elements
                if (debugging) {
                    System.out.println("Received: ");
                    int i;
                    for (i = 0; i < 6; i++) {
                        System.out.print(data[i] + ", ");
                    }
                    System.out.println(data[i]);
                }

                // Parse data
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

                // Build and send result in to byte array
                buildByteArray(result);
                
                if (debugging) {
                    System.out.println("Built Data:");
                    int i;
                    for (i = 0; i < MAX_INT - 1; i++) {
                        System.out.print(bArray[i] + ", ");
                    }
                    System.out.println(bArray[i]);
                }

                bout.write(bArray, 0, bArray.length);
                bout.flush();

                clientSock.close();

            } catch (IOException ex) {
                System.out.println(ex);
                return;
            }
            
            
        }
    }

    private static void buildByteArray(int result) {
        int mask = (int)Math.pow(2,8) - 1;

        for (int i = 0; i < MAX_INT; i++) {
            bArray[i] = (byte)((result >> (i * 8)) & mask);
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

    /**
     * Send "READY" to client to initiate data transfer, and receive the data
     */
    private static void sendReadyGetResponse() {
        try {
            bArray = "READY".getBytes();
            bout.write(bArray, 0, bArray.length);
            bout.flush();

            bin.read(data, 0, 1024);
            if (verbose) System.out.println("Received array of size: " + data.length);
        } catch (IOException ex) {
            System.out.println(ex);
            return;
        }
    }
}