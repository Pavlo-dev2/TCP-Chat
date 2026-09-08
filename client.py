import socket

def getalldata(socket):   
    data = b""
    while b"\r\n\r\n" not in data:
        data = data + socket.recv(1024)
    return data.decode("utf-8")


def request(content):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.sendall(f"{content}\r\n\r\n".encode("utf-8"))
    data = getalldata(sock)
    sock.close()
    return data

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
comand = ""
while (command != "/STOP"):
    #get content
    content = request("CONTENT")#TODO: GET CHAT CONTENT
