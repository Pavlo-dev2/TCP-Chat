import socket

def getalldata(socket):   
    data = b""
    while b"\r\n\r\n" not in data:
        data = data + socket.recv(1024)
    return data.decode("utf-8")

#send request return answer
def request(content):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.settimeout(3.0)
        if content == "STOP":
            quit()
        sock.sendall(f"{content}\r\n\r\n".encode("utf-8"))
        data = getalldata(sock)
        sock.close()
        return data
    except Exception as a:
        if content == "STOP":
            quit()
        return a

#send request dont wait for server answer
def send_request(content):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.settimeout(3.0)
        sock.sendall(f"{content}\r\n\r\n".encode("utf-8"))
        sock.close()
        return 0
    except Exception as a:
        return a


host = input("Enter host: ")
port = int(input("Enter port: "))
name = input("Enter name: ")

#create name
response = ""
while (True):
    try:
        response = request(f"START {name}")
        print(response)
        if response.startswith("Your name is "):
            break
        else:
            if input("Quit?Y/N: ") == "Y":
                quit()
            name = input("Enter name: ")
    except Exception as error:
        print(f"Failed connecting to server, {error}")
        if input("Quit?Y/N:") == "Y":
            quit()
        host = input("Enter host: ")
        port = input("Enter port: ")


#main loop
command = ""
while (True):
    #get content
    content = request("CONTENT")
    print(content)
    command = input("Enter massege(__ to ignore): ")
    if command == "__":
        continue
    elif command == "/STOP":
        break
    send_request(f"POST {command}")

#end sesion with server
send_request("STOP")
