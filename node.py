import socket
import threading

class Node:
    def __init__(self, host, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.data = {}

    def listen(self):
        self.server_socket.listen(5)
        while True:
            client_socket, addr = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        data = client_socket.recv(1024).decode()
        cmd, key, value = data.split('|', 2)
        if cmd == "STORE":
            self.data[key] = value
            client_socket.send("OK".encode())
        elif cmd == "RETRIEVE":
            client_socket.send(self.data.get(key, "NOT FOUND").encode())
        client_socket.close()

    def store(self, host, port, key, value):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        client_socket.send(f"STORE|{key}|{value}".encode())
        response = client_socket.recv(1024).decode()
        client_socket.close()
        return response

    def retrieve(self, host, port, key):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        client_socket.send(f"RETRIEVE|{key}|".encode())
        data = client_socket.recv(1024).decode()
        client_socket.close()
        return data
