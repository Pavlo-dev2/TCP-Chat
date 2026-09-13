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
    
    #print user info
    def print_user(self):
        print(self.ip_address)
        print(self.name)
        print(self.timestamp)

#get all data from client
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

#check if user is active
def in_active_users(name):
    for u in active_users:
        if name == u.name:
            return True
    return False

#return content text
def collect_content():
    content = ""
    for m in masseges:
        content += (m + "\n")
    return content

#check if ip nis active
def in_active_users_ip(ip):
    for u in active_users:
        if ip == u.ip_address:
            return True
    return False

#delate user with ip
def delate_user(ip):
    i = 0
    for u in active_users:
        if u.ip_address == ip:
            print(f"Delating user {u.name}")
            active_users.pop(i)
            return 0
    return 1

#update time by user
def update_time(ip):
    for u in active_users:
        if u.ip_address == ip:
            u.timestamp = time.time()
            return 0
    return 1

def return_name(ip):
    for u in active_users:
        if u.ip_address == ip:
            return u.name
    return 0

host = input("Enter host: ")
port = input("Enter port: ")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, int(port)))
print("Server started")

#active user list
active_users = []

#list of masseges(content)
masseges = ["Pavlo: Hi!", "Pasha: Hello!"]

s.listen(1)
while (True):
    client_socket, client_address = s.accept()
    client_socket.settimeout(10.0)
    print(f"Connection from {client_address} has been established!")
    c_data = getalldata(client_socket)
    #add new user to room
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
    #Prozess content request
    elif c_data.startswith("CONTENT"):
        update_time(client_address[0])
        send_response(client_socket, collect_content())
    #Prozess user stop request 
    elif c_data.startswith("STOP"):
        if in_active_users_ip(client_address[0]):
            delate_user(client_address[0])
    #Prozess user post massage request
    elif c_data.startswith("POST"):
        print("PROZESS")
        print(client_address)
        if in_active_users_ip(client_address[0]):
            try:
                print(c_data)
                massege = re.findall(r"POST (\S+)\r\n\r\n", c_data)[0]
                masseges.append(f"{return_name(client_address[0])}: {massege}")
            except Exception as e:
                print(e)
                continue


