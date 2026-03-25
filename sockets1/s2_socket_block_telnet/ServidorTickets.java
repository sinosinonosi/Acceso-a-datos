package s2_socket_block_telnet;

import java.io.*;
import java.net.*;

public class ServidorTickets {
    public static void main(String[] args) {
        int ticket = 1;
        try (ServerSocket serverSocket = new ServerSocket(9090)) {
            System.out.println("Servidor de tickets iniciado en puerto 9090...");
            
            while (true) {
                Socket socket = serverSocket.accept();
                System.out.println("Cliente conectado. Esperando petición...");

                BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                PrintWriter out = new PrintWriter(socket.getOutputStream(), true);

                String peticion = in.readLine();
                
                if (peticion != null && peticion.equalsIgnoreCase("dame ticket")) {
                    out.println("Tu ticket es: " + ticket);
                    System.out.println("Ticket " + ticket + " entregado.");
                    ticket++;
                }
                socket.close();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}