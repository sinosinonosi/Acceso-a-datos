package s6_sockets_Apache_vs_Nginx;

import java.io.*;
import java.net.*;

public class ClientePrueba {
    public static void main(String[] args) {
        int puertoAProbar = 8081; 
        int numPeticiones = 50;

        System.out.println("Lanzando " + numPeticiones + " peticiones al puerto " + puertoAProbar + "...");

        for (int i = 0; i < numPeticiones; i++) {
            final int id = i;
            new Thread(() -> {
                try (Socket socket = new Socket("localhost", puertoAProbar)) {
                    PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
                    BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));

                    out.println("GET / HTTP/1.1");
                    
                    String linea;
                    while ((linea = in.readLine()) != null) {
                        if (linea.contains("Hola desde")) {
                            System.out.println("Cliente " + id + " recibió: " + linea);
                            break;
                        }
                    }
                } catch (IOException e) {
                    System.out.println("Error en cliente " + id);
                }
            }).start();
        }
    }
}