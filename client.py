import socket

SERVER_ADDRESS = ("192.168.160.28", 5050)

def send(msg):
    message = msg.encode("utf-8")
    msg_length = len(message)
    send_length = str(msg_length).encode("utf-8")
    send_length += b' ' * (64 - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode("utf-8"))


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(SERVER_ADDRESS)
print(f"You are connected to {SERVER_ADDRESS}.\n * '!q' to disconnect\n * '!stop' to stop the server")

getting_input = True
while getting_input:
    prompt = input(" > ")

    # client side prompt processing
    if prompt == "!q":
        getting_input = False

    send(prompt)

