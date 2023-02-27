import socket
import threading
import os

from util import generate_username, format_addr, get_time

# TODO: handle disconnetions, split packages in two (bytes and message itself), move server prints to logger?, send chat history to new client


HOST_NAME = socket.gethostname()
SERVER_HOST = socket.gethostbyname(HOST_NAME)
SERVER_PORT = 5050
SERVER_ADDRESS = (SERVER_HOST, SERVER_PORT)

os.system('cls')
print(HOST_NAME, SERVER_HOST, SERVER_PORT)


class Server:

    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind(SERVER_ADDRESS)

        self.connections = []
        self.conn_threads = []

        self.running = False

        self.chat_history = []

    def start(self):
        self._socket.listen()
        print(f"[SERVER] Server is listening on {format_addr(SERVER_ADDRESS)}...")
        self.running = True
        while self.running:

            conn, addr = self._socket.accept()
            self.connections.append((conn, addr))

            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            self.conn_threads.append(thread)
            thread.start()

            # print(f"[SERVER] Total connections: {threading.active_count() - 1}")
            # self.print_running_threads()

        self._stop_threads()
        self.close_all_connections()

    def stop(self):
        print("[SERVER] Stopping server...")  # TODO: fix can't stop server cause accept() is blocking loop
        self.running = False

    def _stop_threads(self):
        for thread in self.connections:
            thread.stop()

    def handle_client(self, conn, addr):
        username = generate_username()
        print(f"[SERVER] {username} ({format_addr(addr)}) connected.")
        conn.send(username.encode())
        connected = True
        while connected:

            # message header
            # msg_length = conn.recv(64).decode("utf-8")
            # if msg_length:
                # msg_length = int(msg_length)

            # msg = conn.recv(msg_length).decode("utf-8")
            msg = conn.recv(2048).decode()

            # server side prompt processing
            if msg == "!q":
                connected = False
            elif msg == "!stop":
                self.stop()
            else:

                # on success
                chat_line = f"{get_time()} {username}: {msg}"
                self.chat_history.append(chat_line)
                print(chat_line)
                for connection, address in self.connections:
                    # print(f"[SERVER] Sending message ({chat_line}) to ({format_addr(address)})...")
                    connection.send(chat_line.encode())

        conn.close()
        print(f"[SERVER] {username} ({format_addr(addr)}) disconnected.")
        # print(f"[SERVER] Total connections: {threading.active_count() - 1}")

    def update_clients(self, msg):
        for conn in self.connections:
            conn.send(msg)

    def print_running_threads(self):
        for thread in threading.enumerate():
            print(thread.name)

    def close_all_connections(self):
        for connection in self.connections:
            connection.close()

print("[SERVER] Server is starting...")
Server().start()
