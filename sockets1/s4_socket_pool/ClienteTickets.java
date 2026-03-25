package s4_socket_pool;

import java.io.*;
import java.net.*;

public class ClienteTickets {
    public static void main(String[] args) {
        try (Socket socket = new Socket("localhost", 9090)) {
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));

            System.out.println("Pidiendo ticket al servidor...");
            out.println("Dame ticket");

            String respuesta = in.readLine();
            System.out.println("El servidor responde: " + respuesta);
        } catch (IOException e) {
            System.out.println("Error de conexión al pedir el ticket.");
        }
    }
}