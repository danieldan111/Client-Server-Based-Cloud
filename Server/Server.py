import socket
import threading
import time

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DIS_MSG"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"NEW CONNECTION {addr} connected.")

    connected = True
    while connected:
        file_name = conn.recv(100).decode()
        file_size = conn.recv(100).decode()

        # Opening and reading file.
        with open(file_name, "wb") as file:
            size = 0
            # Starting the time capture.
            start_time = time.time()

            # Running the loop while file is recieved.
            while size <= int(file_size):
                data = conn.recv(1024)
                if not (data):
                    break
                file.write(data)
                size += len(data)

            # Ending the time capture.
            end_time = time.time()

        print("File transfer Complete.Total time: ", end_time - start_time)
        
        connected = False

    
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