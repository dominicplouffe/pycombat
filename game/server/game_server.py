import socket

import socket
import threading


class GameServer:
    def __init__(self, host="127.0.0.1", port=65432) -> None:
        self.host = host
        self.port = port
        self.message_len = 1024
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lobbies = {}

    def handle_client(self, conn, addr):
        print(f"New connection: {addr}")
        try:
            while True:
                data = conn.recv(self.message_len)
                if not data:
                    break

                message = self.get_and_clean_message(data)
                command = message.split(" ")[0]

                if command == "create":
                    lobby_name = data.decode("utf-8").split(" ")[1]
                    message = self.create_lobby(lobby_name)
                    self.send_message(conn, message)
                elif command == "join":
                    lobby_name = data.decode("utf-8").split(" ")[1]
                    username = data.decode("utf-8").split(" ")[2]
                    message = self.join_lobby(lobby_name, username, conn)
                    self.send_message(conn, message)
                elif command == "list":
                    message = "Lobbies:\n"
                    for lobby in self.lobbies:
                        message += f"{lobby}\n"
                    self.send_message(conn, message)
                elif command == "update":
                    lobby_name = data.decode("utf-8").split(" ")[1]
                    username = data.decode("utf-8").split(" ")[2]
                    x = data.decode("utf-8").split(" ")[3]
                    y = data.decode("utf-8").split(" ")[4]

                    message = f"update {lobby_name} {username} {x} {y}"
                    for user, user_conn in self.lobbies[lobby_name].items():
                        if user_conn != conn:
                            self.send_message(user_conn, message)
                elif command == "quit":
                    break
                else:
                    print(f"Invalid message: {data.decode('utf-8')}")
        except Exception as e:
            print(f"Error handling message from {addr}: {e}")
        finally:
            conn.close()

    def start(self) -> None:
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Server listening on {self.host}:{self.port}")

        try:
            while True:
                conn, addr = self.server_socket.accept()
                client_thread = threading.Thread(
                    target=self.handle_client, args=(conn, addr)
                )
                client_thread.start()
        except KeyboardInterrupt:
            print("Server is shutting down.")
        finally:
            self.server_socket.close()

    def send_message(self, conn, message: str) -> None:
        num_periods = (self.message_len - 1) - len(message)
        message += "`" * num_periods
        conn.sendall(f"{message}\n".encode("utf-8"))

    def get_and_clean_message(self, data: str) -> str:
        message = data.decode("utf-8")
        message = message.split("\n")
        message = message[0]
        return message.replace("`", "")

    def create_lobby(self, lobby_name) -> None:
        if lobby_name in self.lobbies:
            return "Lobby already exists."

        self.lobbies[lobby_name] = {}

        return "Lobby created."

    def join_lobby(self, lobby_name, username, conn) -> None:
        if lobby_name not in self.lobbies:
            self.lobbies[lobby_name] = {}

        self.lobbies[lobby_name][username] = conn
        self.lobbies[lobby_name] = {
            kk: vv for kk, vv in self.lobbies[lobby_name].items() if not vv._closed
        }

        return "Joined lobby."


if __name__ == "__main__":
    game_server = GameServer()
    game_server.start()
