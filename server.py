import socket
import threading


HOST_NAME = socket.gethostname()
SERVER_HOST = socket.gethostbyname(HOST_NAME)
SERVER_PORT = 5050
SERVER_ADDRESS = (SERVER_HOST, SERVER_PORT)
print(HOST_NAME, SERVER_HOST, SERVER_PORT)

def generate_username():
    pass


class Server:

    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind(SERVER_ADDRESS)
        self.connections = []  # threads
        self.running = False

    def start(self):
        self._socket.listen()
        print(f"[LISTENING] Server is listening on {SERVER_ADDRESS}")
        self.running = True
        while self.running:
            conn, addr = self._socket.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            self.connections.append(thread)
            thread.start()
            print(f"[ACTIVE CONNECTION] {threading.active_count() - 1}")

    def stop(self):
        self.running = False
        for thread in self.connections:
            thread.stop()

    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        connected = True
        while connected:

            # message header
            msg_length = conn.recv(64).decode("utf-8")
            if msg_length:
                msg_length = int(msg_length)

                msg = conn.recv(msg_length).decode("utf-8")

                # server side prompt processing
                if msg == "!q":
                    print(f"[{addr}] Client disconnected.")
                    connected = False
                elif msg == "!stop":
                    self.stop()
                else:
                    print(f"[{addr}] {msg}")
                conn.send("Msg recieved".encode("utf-8"))

        conn.close()

print("[STARTING] Server is starting...")
Server().start()
