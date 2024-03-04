import threading
import socket


class TCPClientThread(threading.Thread):
    def __init__(self, host: str = "127.0.0.1", port: int = 65432) -> None:
        super().__init__()
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = False
        self.update_callback = None
        self.message_len = 1024

    def run(self) -> None:
        try:
            self.client_socket.connect((self.host, self.port))
            self.running = True
            print("Connected to the server.")

            # Start the listening thread
            listening_thread = threading.Thread(target=self.listen_for_messages)
            listening_thread.start()
        except Exception as e:
            print(f"Error connecting to server: {e}")
            self.running = False

    def listen_for_messages(self) -> None:
        while self.running:
            try:
                data = self.client_socket.recv(self.message_len)
                if not data:
                    break

                message = self.get_and_clean_message(data)
                command = message.split(" ")[0]
                if command == "update":
                    self.update_command(message)
            except Exception as e:
                print(f"Error receiving data: {e}")
            finally:
                pass

    def send_message(self, message: str) -> None:
        if self.running:
            try:
                num_periods = (self.message_len - 1) - len(message)
                message += "`" * num_periods
                self.client_socket.sendall(f"{message}\n".encode("utf-8"))
            except Exception as e:
                print(f"Error sending message: {e}")

    def get_and_clean_message(self, data: str) -> str:
        message = data.decode("utf-8")
        message = message.split("\n")
        message = message[0]
        return message.replace("`", "")

    def stop(self) -> None:
        self.running = False

    def update_command(self, command: str) -> None:
        parameters = command.split(" ")

        if not self.update_callback:
            return

        self.update_callback(float(parameters[3]), float(parameters[4]))


if __name__ == "__main__":
    c = TCPClientThread()
    c.start()

    while True:
        message = input("Enter message: ")
        if message == "quit":
            c.stop()
            c.join()
            break
        c.send_message(message)
