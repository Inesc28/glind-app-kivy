import socket
import threading
import json

users = {}

def handle_client(conn, addr):
    try:
        print(f"Conexión establecida desde {addr}")
        data = conn.recv(1024).decode()
        if data:
            user_data = json.loads(data)
            user_id = user_data["userId"]
            username = user_data.get("username", "Desconocido")
            users[user_id] = {"conn": conn, "addr": addr, "username": username}
            print(f"Usuario {user_id} ({username}) conectado al servidor.")
            conn.settimeout(1.0)
            while True:
                try:
                    data = conn.recv(1024).decode()
                    if not data:
                        break
                    request = json.loads(data)
                    action = request.get("action")
                    if action == "get_connected_users":
                        # Enviar la lista de usuarios conectados
                        connected_users = [
                            {"userId": uid, "username": udata["username"]}
                            for uid, udata in users.items()
                        ]
                        response = {
                            "action": "connected_users",
                            "users": connected_users,
                        }
                        conn.send(json.dumps(response).encode())
                    else:
                        pass
                except socket.timeout:
                    # Si ocurre un timeout, continuamos para verificar la conexión
                    continue
                except ConnectionResetError:
                    # El cliente cerró la conexión abruptamente
                    break
                except Exception as ex:
                    print(f"Error al recibir datos del cliente {user_id}: {ex}")
                    break
        # Eliminar al usuario de la lista al desconectarse
        print(f"Usuario {user_id} desconectado del servidor.")
        if user_id in users:
            del users[user_id]
    except Exception as ex:
        print(f"Error en handle_client: {ex}")
    finally:
        conn.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip_address = "0.0.0.0"
    port = 5051
    server_socket.bind((ip_address, port))
    server_socket.listen(5)
    print(f"Servidor iniciado en {ip_address}:{port}")
    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()