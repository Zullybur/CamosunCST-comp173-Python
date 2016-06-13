package comp173.lab5;

import java.lang.*;
import java.net.*;
import java.io.*;

public class ServerA {
    public static final int MAX_BUFF = 1024;

    public static void main(String[] args) {
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

        Socket clientSock;
        BufferedInputStream bin;
        BufferedOutputStream bout;
        byte[] data = new byte[MAX_BUFF];
        byte[] bArray;
        while(true) {
            try {
                clientSock = serverSock.accept();
                bin = new BufferedInputStream(clientSock.getInputStream());
                bout = new BufferedOutputStream(clientSock.getOutputStream());

                bArray = "READY".getBytes();
                bout.write(bArray, 0, bArray.length);
                bout.flush();

                bin.read(data, 0, 1024);
                System.out.println("Received array of size: " + data.length);

                clientSock.close();

            } catch (IOException ex) {
                System.out.println(ex);
                return;
            }
            for (int i = 0; i < (data[1]/2) + (data[1] % 2 == 0 ? 2 : 3); i++) {
                System.out.println("Received: " + data[i]);
            }
            
        }
    }
}