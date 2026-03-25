package s5_sockets_cliente_multiple;

import java.io.*;
import java.net.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.Set;

public class ClienteAgresivoTickets {
    public static void main(String[] args) {
        int numPeticiones = 100;
        Set<String> ticketsRecibidos = ConcurrentHashMap.newKeySet();

        System.out.println("Lanzando " + numPeticiones + " peticiones simultáneas al puerto 9090...");

        for (int i = 0; i < numPeticiones; i++) {
            new Thread(() -> {
                try (Socket socket = new Socket("localhost", 9090)) {
                    PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
                    BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));

                    out.println("Dame ticket");
                    String respuesta = in.readLine();

                    if (respuesta != null) {
                        String numeroTicket = respuesta.replace("Tu ticket es: ", "");
                        
                        if (!ticketsRecibidos.add(numeroTicket)) {
                            System.err.println("¡ALERTA! Condición de carrera. Ticket repetido detectado: " + numeroTicket);
                        } else {
                            System.out.println("Ticket " + numeroTicket + " recibido correctamente.");
                        }
                    }
                } catch (IOException e) {
                    System.out.println("Error de conexión en uno de los hilos.");
                }
            }).start();
        }
    }
}