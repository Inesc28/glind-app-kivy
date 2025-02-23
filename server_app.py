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
                    data = conn.recv(4096).decode()
                    if not data:
                        break
                    request = json.loads(data)
                    action = request.get("action")
                    if action == "get_connected_users":
                        connected_users = [
                            {"userId": uid, "username": udata["username"]}
                            for uid, udata in users.items()
                        ]
                        response = {
                            "action": "connected_users",
                            "users": connected_users,
                        }
                        conn.send(json.dumps(response).encode())
                    elif action == "screen_request":
                        target_user_id = request.get("targetUserId")
                        if target_user_id in users:
                            target_conn = users[target_user_id]["conn"]
                            screen_request = {
                                "action": "screen_request",
                                "fromUserId": user_id
                            }
                            target_conn.send(json.dumps(screen_request).encode())
                    elif action == "screen_response":
                        target_user_id = request.get("targetUserId")
                        response = request.get("response")
                        target_conn = users[target_user_id]["conn"]
                        screen_response = {
                            "action": "screen_response",
                            "fromUserId": user_id,
                            "response": response
                        }
                        target_conn.send(json.dumps(screen_response).encode())
                    elif action == "screen_frame":
                        target_user_id = request.get("targetUserId")
                        frame_data = request.get("frame")
                        if target_user_id in users:
                            target_conn = users[target_user_id]["conn"]
                            screen_frame = {
                                "action": "screen_frame",
                                "fromUserId": user_id,
                                "frame": frame_data
                            }
                            target_conn.send(json.dumps(screen_frame).encode())
                    else:
                        pass
                except socket.timeout:
                    continue
                except ConnectionResetError:
                    break
                except Exception as ex:
                    print(f"Error al recibir datos del cliente {user_id}: {ex}")
                    break
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