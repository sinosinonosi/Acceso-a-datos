package s7_socket_ApacheFR;

import java.io.*;
import java.net.*;
import java.nio.file.*;
import java.util.Properties;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class MiniApache {
    public static void main(String[] args) {
        int puerto = 8082;
        String directorio = "htdocs";
        try (FileInputStream fis = new FileInputStream("server.conf")) {
            Properties config = new Properties();
            config.load(fis);
            puerto = Integer.parseInt(config.getProperty("puerto", "8082"));
            directorio = config.getProperty("directorio", "htdocs");
        } catch (IOException e) {
            System.out.println("Aviso: server.conf no encontrado, usando valores por defecto.");
        }

        ExecutorService pool = Executors.newFixedThreadPool(10);
        try (ServerSocket serverSocket = new ServerSocket(puerto)) {
            System.out.println("Mini Apache iniciado en el puerto " + puerto);

            while (true) {
                Socket cliente = serverSocket.accept();
                String dirFinal = directorio;
                
                pool.execute(() -> {
                    try (BufferedReader in = new BufferedReader(new InputStreamReader(cliente.getInputStream()));
                         PrintWriter out = new PrintWriter(cliente.getOutputStream(), true);
                         OutputStream outBytes = cliente.getOutputStream()) {

                        String peticion = in.readLine();
                        if (peticion == null) return;
                        
                        try (FileWriter fw = new FileWriter("access.log", true);
                             PrintWriter logWriter = new PrintWriter(fw)) {
                            logWriter.println("IP: " + cliente.getInetAddress().getHostAddress() + " | Petición: " + peticion);
                        }

                        System.out.println("Petición recibida: " + peticion);

                        String archivoSolicitado = peticion.split(" ")[1];
                        if (archivoSolicitado.equals("/")) archivoSolicitado = "/index.html";

                        File archivo = Paths.get(dirFinal, archivoSolicitado).toFile();

                        if (archivo.exists() && !archivo.isDirectory()) {
                            byte[] contenido = Files.readAllBytes(archivo.toPath());

                            String cabeceras = "HTTP/1.1 200 OK\r\n" +
                                               "Content-Type: text/html\r\n" +
                                               "Content-Length: " + contenido.length + "\r\n" + 
                                               "\r\n";
                            outBytes.write(cabeceras.getBytes("UTF-8"));
                            outBytes.write(contenido);
                            outBytes.flush(); 

                        } else {
                            String respuesta404 = "HTTP/1.1 404 Not Found\r\n" +
                                                  "Content-Type: text/html\r\n" +
                                                  "\r\n" +
                                                  "<html><body><h1>404 Archivo no encontrado</h1></body></html>";
                            outBytes.write(respuesta404.getBytes("UTF-8"));
                            outBytes.flush();
                        }
                    } catch (IOException e) {
                        System.out.println("Error procesando web.");
                    } finally {
                        try { cliente.close(); } catch (IOException e) {}
                    }
                });
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
