package s6_sockets_Apache_vs_Nginx;

import java.io.*;
import java.net.*;

public class ServidorApache {
    public static void main(String[] args) {
        try (ServerSocket serverSocket = new ServerSocket(8081)) {
            System.out.println("Servidor 'Apache' (Bloqueante) iniciado en puerto 8081...");

            while (true) {
                Socket socket = serverSocket.accept();
                
                new Thread(() -> {
                    try {
                        BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                        PrintWriter out = new PrintWriter(socket.getOutputStream(), true);

                        String peticion = in.readLine();
                        
                        Thread.sleep(2000); 
                        
                        out.println("HTTP/1.1 200 OK\r\n\r\nHola desde Apache Simulado");
                        socket.close();
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }).start();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}