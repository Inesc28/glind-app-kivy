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

            # Registrar la conexión del usuario
            users[user_id] = {"conn": conn, "addr": addr, "username": username}
            print(f"Usuario {user_id} ({username}) conectado al servidor.")

            # Establecer tiempo de espera para detectar desconexiones
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
                        # Manejar otras acciones si es necesario
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

def register_new_user(email, username, password):
    # Aquí puedes agregar la lógica para registrar un nuevo usuario
    print(f"Registrando usuario: {username}")

def validate_user(username, password):
    # Aquí puedes agregar la lógica para validar un usuario
    if username == "test" and password == "password":
        return "user_id"
    return None

def connect_to_server_threaded(logged_in_user_id, page):
    # Aquí puedes agregar la lógica para conectar al servidor en un hilo separado
    threading.Thread(target=lambda: connect_to_server(logged_in_user_id, page)).start()

def connect_to_server(logged_in_user_id, page):
    # Aquí puedes agregar la lógica para conectar al servidor
    print(f"Conectado al servidor como {logged_in_user_id}")

def get_user_data(logged_in_user_id):
    # Aquí puedes agregar la lógica para obtener los datos del usuario
    return {"id": logged_in_user_id, "user": "test_user"}

def get_connected_users(logged_in_user_id):
    # Aquí puedes agregar la lógica para obtener los usuarios conectados
    return [{"userId": "user1", "username": "usuario1"}, {"userId": "user2", "username": "usuario2"}]

if __name__ == "__main__":
    start_server()
