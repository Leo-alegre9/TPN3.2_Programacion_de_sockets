import socket
import threading

HOST = "127.0.0.1"
PORT = 5000


def recibir_mensajes(cliente):
    while True:
        try:
            mensaje = cliente.recv(1024).decode("utf-8")

            if not mensaje:
                print("\n[INFO] El servidor cerró la conexión.")
                break

            print(f"\n{mensaje}")
            print("> ", end="", flush=True)

        except:
            print("\n[INFO] Se perdió la conexión con el servidor.")
            break


def iniciar_cliente():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        cliente.connect((HOST, PORT))

        print("==============================")
        print("         CLIENTE CHAT")
        print("==============================")

        nombre = input("Ingrese su nombre de usuario: ")

        cliente.send(nombre.encode("utf-8"))

        hilo = threading.Thread(
            target=recibir_mensajes,
            args=(cliente,),
            daemon=True
        )

        hilo.start()

        while True:
            mensaje = input("> ")

            cliente.send(mensaje.encode("utf-8"))

            if mensaje == "/quitar":
                break

    except ConnectionRefusedError:
        print("[ERROR] No se pudo conectar con el servidor.")

    except Exception as error:
        print(f"[ERROR] {error}")

    finally:
        cliente.close()
        print("Cliente desconectado.")


if __name__ == "__main__":
    iniciar_cliente()