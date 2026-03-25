package s3_scocket_block_sync;

import java.io.*;
import java.net.*;

public class ServidorTickets {
    private static int ticketGlobal = 1;

    public static void main(String[] args) {
        try (ServerSocket serverSocket = new ServerSocket(9090)) {
            System.out.println("Servidor de tickets CONCURRENTE iniciado en puerto 9090...");
            
            while (true) {
                Socket socket = serverSocket.accept();
                System.out.println("Nuevo cliente conectado.");

                new Thread(new ManejadorTicket(socket)).start();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static class ManejadorTicket implements Runnable {
        private Socket socket;

        public ManejadorTicket(Socket socket) {
            this.socket = socket;
        }

        public void run() {
            try {
                BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                PrintWriter out = new PrintWriter(socket.getOutputStream(), true);

                String peticion = in.readLine();
                
                if (peticion != null && peticion.equalsIgnoreCase("dame ticket")) {
                    int miTicket;
                    
                    synchronized (ServidorTickets.class) {
                        miTicket = ticketGlobal;
                        ticketGlobal++;
                    }
                    
                    out.println("Tu ticket es: " + miTicket);
                    System.out.println("Ticket " + miTicket + " entregado de forma segura.");
                }
            } catch (IOException e) {
                System.out.println("Error de conexión con un cliente.");
            } finally {
                try {
                    socket.close(); 
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }
}