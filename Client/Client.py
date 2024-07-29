import socket
import os
from pathlib import Path

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
    mode = "upload".encode()
    mode += b' ' * (100 - len(mode)) 
    client.send(mode)

    file_name = os.path.basename(path)
    file_size = os.path.getsize(path)

    send_name = file_name.encode()
    send_name += b' ' * (100 - len(send_name))
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

    msg = client.recv(500).decode()
    print(msg.strip())
    # msg = client.recv(100).decode()
    # print(msg)
    

def download_file(): 
    mode = "download".encode()
    mode += b' ' * (100 - len(mode)) 
    client.send(mode)

    files_amount = int(client.recv(500).decode())
    
    for i in range(files_amount):
        print(client.recv(500).decode().strip())

    file_download = input("enter name of file to download (enter '!exit!' to not download anything): ")
    send_download = file_download.encode()
    send_download += b' ' * (500 - len(send_download))

    client.send(send_download)
    if file_download == '!exit!':
        return
    
    path_exists = client.recv(100).decode().strip()
    if path_exists == 'False':
        print("file not exists check your input!")
        return
    
    file_name = client.recv(100)
    file_name = file_name.decode().strip()

    

    file_size = client.recv(100)
    file_size = file_size.decode()

    downloads_path = str(Path.home() / "Downloads")

    # Opening and reading file.
    with open(downloads_path + "/" + file_name, "wb") as file:
        size = 0
        while size <= int(file_size):
            data = client.recv(1024)
            if not (data):
                break
            file.write(data)
            size += len(data)




def start():
    # path = "C:\\Users\\ADMIN\\Downloads\\mb_driver_612_realtekdch_6.0.9689.1.zip"
    # send_file(path)

    # #checking 2 sends
    # path = "C:\\Users\\ADMIN\\Downloads\\TopSecret.png"
    # send_file(path)

    download_file()

    #disconnect
    disconnect()
    

start()