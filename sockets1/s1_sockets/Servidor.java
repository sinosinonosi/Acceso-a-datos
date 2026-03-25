package s1_sockets;

import java.io.*;
import java.net.*;
import java.util.*;

public class Servidor {
    private static List<PrintWriter> clientes = new ArrayList<>();

    public static void main(String[] args) {
        try (ServerSocket serverSocket = new ServerSocket(8079)) {
            System.out.println("Servidor de Chat iniciado. Esperando clientes...");

            while (true) {
                Socket socket = serverSocket.accept();
                System.out.println("¡Nuevo cliente conectado!");

                new Thread(new ManejadorCliente(socket)).start();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static class ManejadorCliente implements Runnable {
        private Socket socket;
        private PrintWriter out;

        public ManejadorCliente(Socket socket) {
            this.socket = socket;
        }

        public void run() {
            try {
                BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                out = new PrintWriter(socket.getOutputStream(), true);

                synchronized (clientes) {
                    clientes.add(out);
                }

                String mensaje;
                while ((mensaje = in.readLine()) != null) {
                    if (mensaje.equalsIgnoreCase("salir")) {
                        break;
                    }
                    System.out.println("Recibido en servidor: " + mensaje);
                    
                    synchronized (clientes) {
                        for (PrintWriter escritor : clientes) {
                            if (escritor != out) {
                                escritor.println(mensaje);
                            }
                        }
                    }
                }
            } catch (IOException e) {
                System.out.println("Error de conexión con un cliente.");
            } finally {
                if (out != null) {
                    synchronized (clientes) {
                        clientes.remove(out);
                    }
                }
                try {
                    socket.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
                System.out.println("Un cliente ha abandonado el chat.");
            }
        }
    }
}