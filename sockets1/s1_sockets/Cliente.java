package s1_sockets;

import java.io.*;
import java.net.*;
import java.util.Scanner;

public class Cliente {
    public static void main(String[] args) {
        try (Socket socket = new Socket("localhost", 8079)) {
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            Scanner scanner = new Scanner(System.in);

            System.out.print("Escribe tu nickname para entrar al chat: ");
            String nick = scanner.nextLine();

            Thread hiloLectura = new Thread(() -> {
                try {
                    String mensajeServidor;
                    while ((mensajeServidor = in.readLine()) != null) {
                        System.out.println(mensajeServidor);
                    }
                } catch (IOException e) {
                    System.out.println("Desconectado del servidor.");
                }
            });
            hiloLectura.start();

            System.out.println("Conectado como '" + nick + "'. Escribe tus mensajes (escribe 'salir' para terminar):");

            while (true) {
                String mensaje = scanner.nextLine();
                
                if (mensaje.equalsIgnoreCase("salir")) {
                    out.println("salir");
                    break;
                }
                
                out.println(nick + ": " + mensaje);
            }
            
            socket.close(); 
            System.out.println("Conexión cerrada.");
        } catch (IOException e) {
            System.out.println("No se pudo conectar al servidor.");
        }
    }
}