import java.io.*;
import java.net.*;
import java.util.Scanner;

public class ClienteChat {

    public static void main(String[] args) {

        Scanner teclado = new Scanner(System.in);

        System.out.println("==============================");
        System.out.println("       CLIENTE CHAT JAVA");
        System.out.println("==============================");

        System.out.print("Ingrese IP del servidor: ");
        String host = teclado.nextLine();

        System.out.print("Ingrese puerto del servidor: ");
        int puerto;

        try {
            puerto = Integer.parseInt(teclado.nextLine());
        } catch (NumberFormatException e) {
            System.out.println("[ERROR] El puerto ingresado no es válido.");
            teclado.close();
            return;
        }

        try {

            Socket socket = new Socket(host, puerto);

            System.out.println(
                "[SERVIDOR] Conexión establecida correctamente."
            );

            InputStream entrada = socket.getInputStream();

            PrintWriter salida = new PrintWriter(
                new OutputStreamWriter(
                    socket.getOutputStream(),
                    "UTF-8"
                ),
                true
            );

            System.out.print("Ingrese su nombre de usuario: ");
            String nombre = teclado.nextLine();

            salida.println(nombre);

            Thread hiloRecepcion = new Thread(() -> {

                byte[] buffer = new byte[1024];

                try {

                    while (true) {

                        int bytesLeidos = entrada.read(buffer);

                        if (bytesLeidos == -1) {

                            System.out.println(
                                "\n[INFO] El servidor cerró la conexión."
                            );

                            break;
                        }

                        String mensaje = new String(
                            buffer,
                            0,
                            bytesLeidos,
                            "UTF-8"
                        );

                        System.out.println();
                        System.out.println(mensaje);
                        System.out.print("> ");
                    }

                } catch (IOException e) {

                    System.out.println(
                        "\n[INFO] Se perdió la conexión con el servidor."
                    );
                }

            });

            hiloRecepcion.setDaemon(true);
            hiloRecepcion.start();

            while (true) {

                System.out.print("> ");
                String mensaje = teclado.nextLine();

                salida.println(mensaje);

                if (mensaje.equals("/quitar")) {
                    break;
                }
            }

            socket.close();

            System.out.println(
                "Cliente desconectado."
            );

        } catch (ConnectException e) {

            System.out.println(
                "[ERROR] No se pudo conectar con el servidor."
            );

        } catch (UnknownHostException e) {

            System.out.println(
                "[ERROR] La dirección IP o el host ingresado no es válido."
            );

        } catch (IOException e) {

            System.out.println(
                "[ERROR] " + e.getMessage()
            );

        } finally {

            teclado.close();
        }
    }
}