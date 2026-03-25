package s6_sockets_Apache_vs_Nginx;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.util.Iterator;

public class ServidorNginx {
    public static void main(String[] args) throws IOException {
        Selector selector = Selector.open();
        ServerSocketChannel serverSocket = ServerSocketChannel.open();
        serverSocket.bind(new InetSocketAddress(8082));
        
        serverSocket.configureBlocking(false);
        serverSocket.register(selector, SelectionKey.OP_ACCEPT);

        System.out.println("Servidor 'Nginx' (Event-Driven) iniciado en puerto 8082...");

        while (true) {
            selector.select(); 
            Iterator<SelectionKey> iterador = selector.selectedKeys().iterator();

            while (iterador.hasNext()) {
                SelectionKey evento = iterador.next();
                iterador.remove();

                if (evento.isAcceptable()) {
                    SocketChannel cliente = serverSocket.accept();
                    cliente.configureBlocking(false);
                    cliente.register(selector, SelectionKey.OP_READ);
                } 
                else if (evento.isReadable()) {
                    SocketChannel cliente = (SocketChannel) evento.channel();
                    ByteBuffer buffer = ByteBuffer.allocate(1024);
                    int bytesLeidos = cliente.read(buffer);
                    
                    if (bytesLeidos > 0) {
                        String respuesta = "HTTP/1.1 200 OK\r\n\r\nHola desde Nginx Simulado";
                        cliente.write(ByteBuffer.wrap(respuesta.getBytes()));
                        cliente.close();
                    }
                }
            }
        }
    }
}