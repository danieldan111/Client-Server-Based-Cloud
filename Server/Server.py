import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DIS_MSG"

#path to save
PATH = "C:\\Users\\ADMIN\\Documents\\Cloud-Project\\Cloud Storage"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"NEW CONNECTION {addr} connected.")
    connected = True
    
    while connected:
        file_name = conn.recv(100)
        file_name = file_name.decode()
        
        #disconnect
        if file_name.strip() == DISCONNECT_MESSAGE:
            print("conn close")
            connected = False

        elif file_name:
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