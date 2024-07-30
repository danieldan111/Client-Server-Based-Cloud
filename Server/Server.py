import socket
import threading
import os

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DIS_MSG"

#path to store files
PATH = "C:\\Users\\ADMIN\\Documents\\Cloud-Project\\Cloud Storage"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)



def handle_client(conn, addr):
    def get_files():
        count_files = 0
        for file in os.listdir(PATH):
            count_files += 1
        
        send_amount = str(count_files).encode()
        send_amount += b' ' * (500 - len(send_amount))
        conn.send(send_amount)

        for file in os.listdir(PATH):
            fileName = file.encode()
            fileName += b' ' * (500 - len(fileName))
            conn.send(fileName)

    print(f"NEW CONNECTION {addr} connected.")
    connected = True
    
    while connected:
        mode = conn.recv(100).decode()  #client can download or upload
        
        #disconnect
        if mode.strip() == DISCONNECT_MESSAGE:
            print("conn close")
            connected = False

        elif mode.strip() == "upload":

            file_name = conn.recv(100)
            file_name = file_name.decode()

            file_size = conn.recv(100)
            file_size = file_size.decode()

            # Opening and reading file.
            with open(PATH + "/" + file_name, "wb") as file:
                size = 0
                while size <= int(file_size):
                    data = conn.recv(1024)
                    if not (data):
                        break
                    file.write(data)
                    size += len(data)

            
            msg = f"Succsefuly uploaded {file_name}".encode()
            msg += b' ' * (500 - len(msg))
            conn.send(msg)

        elif mode.strip() == "getFiles":
            get_files()


        elif mode.strip() == "download":
            file_name = conn.recv(500).decode().strip()
            if file_name == '!exit!':
                break
            else:                
                path = PATH + "/" + file_name
                isExist = os.path.exists(path)
                
                send_exs = str(isExist).encode()
                send_exs += b' ' * (100 - len(send_exs))
                conn.send(send_exs)
                if not isExist:
                    continue

                file_name = os.path.basename(path)
                file_size = os.path.getsize(path)

                send_name = file_name.encode()
                send_name += b' ' * (100 - len(send_name))
                conn.send(send_name)

                send_size = str(file_size).encode()
                send_size += b' ' * (100 - len(send_size))
                conn.send(send_size)
                with open(path, 'rb') as file:
                    size = 0
                    while size <= file_size:
                        data = file.read(1024)
                        if len(data) < 1024:
                            data += b' ' * (1024 - len(data))
                        if not (data):
                            break
                        conn.send(data)
                        size += len(data)

                sucsses_msg = f"Succsesfully Downloaded {file_name} please check your Downloads folder!"
                send_msg = sucsses_msg.encode()
                send_msg += b' ' * (500 - len(send_msg))
                conn.send(send_msg)
                

    
    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listnening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("Server is starting")
start()