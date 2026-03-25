# Práctica Final: Sockets en Java y Servidores Web

Este repositorio contiene todas las soluciones para la práctica de programación de sockets TCP, concurrencia y simulación de servidores web.

## 📂 Contenido del Repositorio

### 1. Chat Básico Multiusuario
- **`Servidor.java` y `Cliente.java`**: Implementación de un chat cliente-servidor mediante TCP.
- Soporta múltiples mensajes de forma continua mediante bucles de lectura/escritura.
- Cierre ordenado de la conexión al escribir la palabra reservada `salir`.
- **Mejora**: Es totalmente concurrente (multisala usando hilos) y soporta *nicks* de usuario para que varios clientes puedan hablar a la vez. El servidor reenvía el mensaje a todos los clientes excepto al emisor original para evitar ecos.

### 2. Servidor de Tickets (Problemas de Concurrencia)
Implementación de un sistema de cola para demostrar los distintos modelos de concurrencia:
- **Solución 1 (`ServidorTickets.java` / `ClienteTickets.java`)**: Servidor iterativo básico. Demuestra cómo el servidor se bloquea impidiendo nuevas conexiones si un cliente (ej. usando `telnet`) ocupa el socket sin enviar peticiones.
- **Solución 2**: Implementación con concurrencia de hilos (`Thread`) para evitar el bloqueo del *accept()*. Uso del bloque `synchronized` para evitar condiciones de carrera al repartir tickets globales.
- **Solución 3**: Refactorización profesional usando un pool de hilos (`ExecutorService`) para limitar conexiones simultáneas y uso de `AtomicInteger` para un incremento atómico seguro de los tickets.
- **Cliente Agresivo**: Script que lanza decenas de peticiones simultáneas para poner a prueba el servidor y detectar si existe la posibilidad de que se repita el mismo ticket.

### 3. Comparativa Apache vs Nginx
Tres códigos para comprender y demostrar la diferencia de gestión de conexiones:
- **`ServidorApache.java`**: Simula el modelo tradicional (prefork), utilizando I/O bloqueante al asignar un hilo completo dedicado a cada conexión entrante.
- **`ServidorNginx.java`**: Simula el modelo *event-driven* (basado en eventos). Utiliza la librería `java.nio` (Selector) con I/O no bloqueante para gestionar múltiples sockets concurrentes desde un solo hilo (event loop).
- **`ClientePrueba.java`**: Lanza ráfagas de peticiones de prueba contra ambos simuladores.

### 4. Mini Servidor Apache
Un servidor web HTTP completamente funcional programado desde cero en Java simulando el servicio de Apache:
- **`MiniApache.java`**: Código principal que implementa un ServerSocket con un *Pool de threads* para responder peticiones HTTP.
- **`server.conf`**: Fichero de configuración que define el puerto de escucha y el directorio raíz donde buscar los archivos.
- **`htdocs/`**: Directorio raíz que contiene las páginas web (ej. `index.html`), dando soporte a múltiples páginas y gestionando errores 404.
- **Logs**: Generación automática de un archivo `access.log` para registrar las IPs de los clientes y sus peticiones HTTP.

### ⚠️ Nota importante de ejecución (Mini Apache)
El código de `MiniApache.java` utiliza rutas relativas para leer el archivo de configuración y servir la web. Dependiendo del IDE (NetBeans, Eclipse, etc.) o si se ejecuta desde terminal, el directorio base puede variar. 
Si al arrancar el servidor aparece el aviso *"server.conf no encontrado"*, asegúrate de que el archivo `server.conf` y la carpeta `htdocs` estén situados directamente en la carpeta raíz desde donde se está ejecutando el proyecto (o modifica la ruta en el código para que apunte a la subcarpeta correspondiente).

---

## 🔍 Análisis del uso de Sockets en el código real de Apache (httpd)
*Respuesta al requerimiento de investigación sobre el repositorio oficial (https://github.com/apache/httpd).*

Revisando el código fuente en C del servidor HTTP Apache real, el uso a bajo nivel de la API de sockets se concentra en dos grandes operaciones clave:

1. **Creación y configuración del Socket (`bind` y `listen`):**
   La preparación inicial para que el servidor cree el descriptor del socket y comience a escuchar en los puertos correspondientes (como el 80 o el 443) se gestiona principalmente dentro de los archivos ubicados en `server/listen.c`. Aquí se encuentran las funciones internas que levantan los *listeners*.

2. **Aceptación de conexiones (`accept`):**
   El momento exacto en el que el servidor acepta la conexión entrante de un cliente depende de la arquitectura o Módulo de Multiprocesamiento (MPM) que esté configurado:
   - En el modelo tradicional de asignación de procesos/hilos bloqueantes (Prefork/Worker), la llamada a `accept()` ocurre dentro de los archivos específicos del módulo, concretamente en `server/mpm/prefork/prefork.c`.
   - En el modelo más moderno orientado a eventos (Event), el cual utiliza mecanismos del sistema operativo para I/O no bloqueante como `epoll` (Linux) o `kqueue`, la gestión y aceptación de las conexiones se centraliza en el archivo `server/mpm/event/event.c`.