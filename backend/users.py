import socket
import threading
import string
import random
import json

users = {
    "VE0001ABC": {
        "email": "sant@gmail.com",
        "user": "sant04",
        "password": "12345",
        "linked_devices": ["VE0002DEF"],
    },
    "VE0002DEF": {
        "email": "acness@hotmail.com",
        "user": "acness08",
        "password": "67890",
        "linked_devices": ["VE0001ABC", "VE0003GHI"],
    },
    "VE0003GHI": {
        "email": "sidness@example.com",
        "user": "sidness26",
        "password": "98765",
        "linked_devices": ["VE0001ABC"],
    },
}


def generate_user_id(pais="VE"):
    nums = "".join(random.choices(string.ascii_uppercase, k=4))
    ch = "".join(random.choices(string.digits, k=4))
    return f"{pais}{nums}{ch}"


def register_new_user(email, user, password):
    asignedId = generate_user_id()
    while asignedId in users:
        register_new_user(email, user, password)
    users[asignedId] = {"email": email, "user": user, "password": password}
    print(users)


def validate_user(user, password):
    for userId, user_data in users.items():
        if user == user_data["user"] and password == user_data["password"]:
            print("Inicio de sesión exitoso")
            return userId  # Devuelves el ID del usuario
        elif user == user_data["user"]:
            print("La contraseña es incorrecta.")
            return None
    print("El usuario ingresado no existe.")
    return None

def get_user_data(user_id):
    if user_id in users:
        return {"id": user_id, "user": users[user_id]["user"]}
    else:
        return None


client_sockets = {}

def connect_to_server(logged_in_user_id, _):
    try:
        server_ip = "127.0.0.1"  # Reemplaza con la IP del servidor si es necesario
        server_port = 5051  # Puerto del servidor
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
        print(f"Conectado al servidor en {server_ip}:{server_port}")
        # Enviar el userId y username al servidor
        user_info = get_user_data(logged_in_user_id)
        if user_info:
            user_data = {"userId": logged_in_user_id, "username": user_info["user"]}
            client_socket.send(json.dumps(user_data).encode())
        else:
            print("No se pudo obtener información del usuario")
            return
        # Almacenar el socket del cliente
        client_sockets[logged_in_user_id] = client_socket
    except Exception as ex:
        print(f"Error al conectar al servidor: {ex}")


def disconnect_from_server(logged_in_user_id):
    try:
        client_socket = client_sockets.get(logged_in_user_id)
        if client_socket:
            # Enviar una señal de desconexión al servidor (opcional)
            # request = {"action": "disconnect"}
            # client_socket.send(json.dumps(request).encode())
            client_socket.close()
            del client_sockets[logged_in_user_id]
            print(f"Desconectado del servidor.")
        else:
            print("No hay conexión al servidor para desconectar.")
    except Exception as ex:
        print(f"Error al desconectar del servidor: {ex}")


def connect_to_server_threaded(logged_in_user_id, page):
    threading.Thread(target=connect_to_server, args=(logged_in_user_id, page)).start()

def get_connected_users(logged_in_user_id):
    try:
        client_socket = client_sockets.get(logged_in_user_id)
        if client_socket:
            # Enviar solicitud al servidor
            request = {"action": "get_connected_users"}
            client_socket.send(json.dumps(request).encode())
            # Establecer tiempo de espera para la respuesta
            client_socket.settimeout(5)
            # Recibir respuesta del servidor
            response_data = client_socket.recv(4096).decode()
            response = json.loads(response_data)
            if response.get("action") == "connected_users":
                connected_users = response.get("users", [])
                return connected_users
            else:
                print("Respuesta desconocida del servidor")
                return []
        else:
            print("No hay conexión al servidor")
            return []
    except socket.timeout:
        print("Tiempo de espera agotado al recibir respuesta del servidor")
        return []
    except Exception as ex:
        print(f"Error en get_connected_users: {ex}")
        return []