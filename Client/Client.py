import socket
import os
import time

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DIS_MSG"
SERVER = "10.0.0.21"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


# def end(msg):
#     message = msg.encode(FORMAT)
#     msg_length = len(message)
#     send_length = str(msg_length).encode(FORMAT)
#     send_length += b' ' * (HEADER - len(send_length))
#     client.send(send_length)
#     client.send(message)

file_name = "SnapCameraPreservation-main.zip"
file_size = os.path.getsize(file_name)

send_name = file_name.encode()
send_name += b' ' * (100 - len(send_name))
client.send(send_name)

send_size = str(file_size).encode()
send_size += b' ' * (100 - len(send_size))
client.send(send_size)



with open(file_name, "rb") as file:
    size = 0
    # Starting the time capture.
    start_time = time.time()

    while size <= file_size:
        data = file.read(1024)
        if not (data):
            break
        client.sendall(data)
        size += len(data)

    # Ending the time capture.
    end_time = time.time()

print("File Transfer Complete.Total time: ", end_time - start_time)

client.close()

