import socket
import time
import re

#the user class is used to create a user object that can be used to store user information
class user:
    type = "user"
    def __init__(self, ip_address=None, name=None, timestamp=None):
        self.ip_address = ip_address
        self.name = name
        self.timestamp = time.time() if timestamp is None else timestamp
    
    def print_user(self):
        print(self.ip_address)
        print(self.name)
        print(self.timestamp)

def getalldata(client_socket):   
    print("\n===Receiving data from client...===\n")
    data = b""
    while b"\r\n\r\n" not in data:
        data = data + client_socket.recv(1024)
    print(data.decode("utf-8"))
    return data.decode("utf-8")

def send_response(client_socket, content):
    client_socket.sendall(f"{content}\r\n\r\n".encode("utf-8"))
    client_socket.close()

def in_active_users(name):
    for u in active_users:
        if name == u.name:
            return True
    return False


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 8080))
print("Server started")

active_users = []

s.listen(1)
while (True):
    client_socket, client_address = s.accept()
    client_socket.settimeout(10.0)
    print(f"Connection from {client_address} has been established!")
    c_data = getalldata(client_socket)
    if c_data.startswith("START "):
        if len(active_users) >= 15:
            send_response(client_socket, "Server is full")
        name = re.findall("START (.*?)\r\n\r\n", c_data)[0]
        if len(name) < 3:
            send_response(client_socket, "Name is too short")
        elif len (name) > 10:
            send_response(client_socket, "Name is too long")
        elif in_active_users(name):
            send_response(client_socket, "This name is already taken")
        else:
            active_users.append(user(ip_address=client_address[0], name=name, timestamp=time.time()))
            send_response(client_socket, f"Your name is {name}")
            for u in active_users:
                u.print_user()
        #TODO PROZESS CONTENT REQUEST
