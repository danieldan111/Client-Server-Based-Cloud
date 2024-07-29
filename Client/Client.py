import socket
import os


HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DIS_MSG"
SERVER = "10.0.0.21"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def disconnect():
    print("disconnecting")
    disconn = DISCONNECT_MESSAGE.encode(FORMAT) 
    disconn += b' ' * (100 - len(disconn))
    client.send(disconn)
    client.close()


def send_file(path):
    file_name = os.path.basename(path)
    file_size = os.path.getsize(path)

    send_name = file_name.encode()
    send_name += b' ' * (100 - len(send_name))
    print(send_name)
    client.send(send_name)

    send_size = str(file_size).encode()
    send_size += b' ' * (100 - len(send_size))
    client.send(send_size)


    with open(path, "rb") as file:
        size = 0
        
        while size <= file_size:
            data = file.read(1024)
            if len(data) < 1024:
                data += b' ' * (1024 - len(data))
            if not (data):
                break
            client.send(data)
            size += len(data)

    
    
    


def start():
    
    path = "C:\\Users\\ADMIN\\Downloads\\mb_driver_612_realtekdch_6.0.9689.1.zip"
    send_file(path)
    
    #checking 2 sends
    path = "C:\\Users\\ADMIN\\Downloads\\TopSecret.png"
    send_file(path)

    #disconnect
    disconnect()
    

start()