import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

clientes = []
usuarios = {}


def enviar_a_todos(mensaje, cliente_origen=None):
    for cliente in clientes.copy():
        if cliente != cliente_origen:
            try:
                cliente.send(mensaje.encode("utf-8"))
            except:
                eliminar_cliente(cliente)


def eliminar_cliente(cliente):
    if cliente in clientes:
        clientes.remove(cliente)

    nombre = usuarios.pop(cliente, "Usuario desconocido")

    try:
        cliente.close()
    except:
        pass

    print(f"[DESCONECTADO] {nombre}")

    enviar_a_todos(
        f"[SERVIDOR] {nombre} se desconectó del chat."
    )


def manejar_cliente(cliente, direccion):
    try:
        nombre = cliente.recv(1024).decode("utf-8").strip()

        if not nombre:
            cliente.close()
            return

        clientes.append(cliente)
        usuarios[cliente] = nombre

        print(f"[NUEVO CLIENTE] {nombre} - {direccion}")

        cliente.send(
            "[SERVIDOR] Conexión establecida correctamente.".encode("utf-8")
        )

        enviar_a_todos(
            f"[SERVIDOR] {nombre} ingresó al chat.",
            cliente
        )

        while True:
            mensaje = cliente.recv(1024).decode("utf-8")

            if not mensaje:
                break

            mensaje = mensaje.strip()

            if mensaje == "/listar":
                lista = ", ".join(usuarios.values())

                cliente.send(
                    f"[SERVIDOR] Usuarios conectados: {lista}".encode("utf-8")
                )

            elif mensaje == "/quitar":
                break

            else:
                mensaje_completo = f"[{nombre}] {mensaje}"

                print(mensaje_completo)

                enviar_a_todos(
                    mensaje_completo,
                    cliente
                )

    except (ConnectionResetError, ConnectionAbortedError):
        pass

    except Exception as error:
        print(f"[ERROR] Cliente {direccion}: {error}")

    finally:
        eliminar_cliente(cliente)


def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        servidor.bind((HOST, PORT))
        servidor.listen()

        print("================================")
        print("       SERVIDOR DE CHAT")
        print("================================")
        print(f"Puerto: {PORT}")
        print("Esperando conexiones...")
        print()

        while True:
            cliente, direccion = servidor.accept()

            hilo = threading.Thread(
                target=manejar_cliente,
                args=(cliente, direccion),
                daemon=True
            )

            hilo.start()

            print(
                f"[CONEXIONES ACTIVAS] {threading.active_count() - 1}"
            )

    except OSError as error:
        print(f"[ERROR DEL SERVIDOR] {error}")

    finally:
        servidor.close()


if __name__ == "__main__":
    iniciar_servidor()