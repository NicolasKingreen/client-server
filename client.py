import socket
import threading
import os
import re
from time import sleep

from util import format_addr

SERVER_HOST = ""
SERVER_ADDRESS = (SERVER_HOST, 5050)
MESSAGE_STARTS_WITH_TIMESTEMP_PATTERN = r'\d{2}:\d{2}:\d{2} *'


class Client:
    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

        self.update_thread = threading.Thread(target=self.update)
        self.cli_thread = threading.Thread(target=self.draw_interface)

        self.getting_input = False
        self.got_new_message = False


        self.chat_history = []  # one entry = one message

    def connect(self, addr):
        self._socket.connect(addr)
        self.connected = True

        os.system('cls')
        conn_str = f"You are connected to {format_addr(SERVER_ADDRESS)}."
        self.chat_history.append(conn_str)
        print(conn_str)

        self.username = self._socket.recv(2048).decode()
        usr_str = f"Your username: {self.username}"
        self.chat_history.append(usr_str)
        print(usr_str)

    def start(self):

        if self.connected:
            self.update_thread.start()
            self.cli_thread.start()

            cmnds_str = " * '!q' to disconnect\n * '!stop' to stop the server"
            self.chat_history.append(cmnds_str)
            print(cmnds_str)

            print(" > ", end='')
            self.getting_input = True

        while self.connected:
            if self.getting_input:
                self.get_input()

        self._socket.close()

    def get_input(self):
        prompt = input()

        # client side prompt processing
        if prompt == "!q":
            self.getting_input = False
            self.connected = False

        self.send(prompt)

    def print_chat_history(self):
        for message in self.chat_history:
            print(message)

    def send(self, message):
        # message = msg.encode()
        # msg_length = len(message)
        # send_length = str(msg_length).encode("utf-8")
        # send_length += b' ' * (64 - len(send_length))
        self._socket.send(message.encode())

    def update(self):
        """
        Processes server messages. If it starts with timestemp, then it's added to the client's history.
        """
        while self.connected:
            if not self.got_new_message:
                new_message = self._socket.recv(2048).decode()
                if re.match(MESSAGE_STARTS_WITH_TIMESTEMP_PATTERN, new_message):
                    self.chat_history.append(new_message)
                    self.got_new_message = True

    def draw_interface(self):
        while self.connected:
            if self.got_new_message:
                os.system('cls')
                self.print_chat_history()
                print(" > ")  # TODO: fix prompt doesn't appear inline with input
                self.got_new_message = False



if __name__ == "__main__":
    client = Client()
    client.connect(SERVER_ADDRESS)
    client.start()
