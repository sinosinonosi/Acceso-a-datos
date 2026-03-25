package s4_socket_pool;

import java.io.*;
import java.net.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicInteger;

public class ServidorTickets {
    private static AtomicInteger ticketGlobal = new AtomicInteger(1);

    public static void main(String[] args) {
        ExecutorService pool = Executors.newFixedThreadPool(5);

        try (ServerSocket serverSocket = new ServerSocket(9090)) {
            System.out.println("Servidor de tickets con POOL DE HILOS iniciado (Puerto 9090)...");
            
            while (true) {
                Socket socket = serverSocket.accept();
                System.out.println("Nuevo cliente conectado.");

                pool.execute(new ManejadorTicket(socket));
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            pool.shutdown();
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
                    int miTicket = ticketGlobal.getAndIncrement();
                    
                    out.println("Tu ticket es: " + miTicket);
                    System.out.println("Ticket " + miTicket + " entregado.");
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