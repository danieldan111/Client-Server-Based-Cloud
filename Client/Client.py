import socket
import os
from pathlib import Path
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import customtkinter


PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DIS_MSG"
SERVER = "10.0.0.21"
ADDR = (SERVER, PORT)

window = tk.Tk()
#getting screen width and height of display
width= window.winfo_screenwidth() 
height= window.winfo_screenheight()
#setting tkinter window size
window.geometry("%dx%d" % (width, height))
window.state('zoomed')

# window.geometry(f"{width}x{height}")
window.title("Client-UI")

#window-props
window.config(background="#161625")


#headline
label = Label(window, text="Famliy Cloud", font=('Arial', 35),bg='#161625', fg='White')
label.pack(pady=50)

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
    return msg.strip()
    
    

def download_file(fl_name): 
    mode = "download".encode()
    mode += b' ' * (100 - len(mode)) 
    client.send(mode)

    # files_amount = int(client.recv(500).decode())
    
    # for i in range(files_amount):
    #     print(client.recv(500).decode().strip())

    # file_download = input("enter name of file to download (enter '!exit!' to not download anything): ")
    file_download = fl_name
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

    msg = client.recv(500).decode()
    print("msg is " + msg.strip())
    return msg.strip()


def clear_sc():
    for widget in window.winfo_children():
        try:
            if widget.cget("text") == 'Famliy Cloud':
                continue
            else:
                widget.destroy()
        except Exception:
            widget.destroy()

def upload_page():
    clear_sc()

    def clearPath():
        path_entry.config(state=NORMAL)
        path_entry.delete(0,END)
    def browse_button():
        # Allow user to select a directory and store it in global var
        # called folder_path
        path_entry.config(state=NORMAL)
        filename = filedialog.askopenfilename(parent=window,title="Browse File")   
        path_entry.delete(0,END)
        path_entry.insert(0, filename)
    def upload():
        path = path_entry.get()
        if os.path.exists(path):
            msg = send_file(path)
            msg_label.config(text=msg)
        else:
            msg_label.config(text="path doesn't exsits") 
    
    top_frame = Frame(window, width=width, height=450, bg="#161625")
    top_frame.pack()

    frame1 = Frame(top_frame, width=width, height=200, bg="#161625")
    frame1.pack()

    path_margin = Label(frame1, text="", height=1, bg="#161625")
    path_margin.pack()
    #path label
    path_label = Label(frame1, text="File to Upload", font=('Arial', 20),bg='#161625', fg='White')
    path_label.pack(side=TOP, anchor=NW)
    #path type
    path_entry = Entry(frame1, font=("Arial", 23),width= 40)
    path_entry.pack(side=LEFT)
    #btn margin
    path_btn_margin = Label(frame1, text="", width=1, bg="#161625")
    path_btn_margin.pack(side=LEFT)
    #path select
    path_select = Button(frame1,text="Browse", font=("Arial", 15),width= 7,height=1,command=browse_button)
    path_select.pack(side=LEFT)
    keys_margin_1 = Label(frame1, text="", width=1, bg="#161625")
    keys_margin_1.pack(side=LEFT)
    ##clear path
    clear_path_btn = Button(frame1, text="Clear", font=("Arial", 15), width= 7,height=1 ,command=clearPath)
    clear_path_btn.pack(side=LEFT)

    frame2 = Frame(top_frame, width=width, height=200, bg="#161625")
    frame2.pack()

    scan_marg_top = Label(frame2, text="", height=5, bg="#161625")
    scan_marg_top.pack()
    
    #scan btn
    scan_btn = Button(frame2, text="Upload", font=("Arial", 23) ,command=upload)
    scan_btn.pack()

    back_btn = Button(window, text="Back To Menu", font=("Arial", 23) ,command=main_page)
    back_btn.pack(side=BOTTOM,anchor=SW,padx=30, pady=30)

    msg_label = Label(frame2, text="", font=('Arial', 20),bg='#161625', fg='White')
    msg_label.pack()

def download_page():
    def opt(btn):
        global selection
        selection = btn
        
        for widget in files_scroll.winfo_children():
            if widget != btn:
                widget.configure(fg_color="#161625", text_color="white")
            else:
                widget.configure(fg_color="white", text_color="black")  
        
    def show():
        msg = download_file(selection.cget("text"))
        msg_label.config(text=msg)

    def add_file(name):
        file_label = customtkinter.CTkButton(files_scroll, text=name,font=('Arial', 20),fg_color="#161625",text_color="white")
        file_label.configure(command=lambda: opt(file_label))
        file_label.pack()
    
    clear_sc()

    files_frame = Frame(window, bg="#161625")
    files_frame.pack()


    files_scroll = customtkinter.CTkScrollableFrame(files_frame, width=500, height=500)
    files_scroll.pack(pady=40)


    mode = "getFiles".encode()
    mode += b' ' * (100 - len(mode)) 
    client.send(mode)

    files_amount = int(client.recv(500).decode())
    
    var = StringVar()
    for i in range(files_amount):
        file_name = client.recv(500).decode().strip()
        add_file(file_name)
        

    
    download_btn = Button(files_frame, text="Download", font=("Arial", 23) ,command=show)
    download_btn.pack(padx=30, pady=30)

    back_btn = Button(window, text="Back To Menu", font=("Arial", 23) ,command=main_page)
    back_btn.pack(side=BOTTOM,anchor=SW,padx=30, pady=30)

    msg_label = Label(files_frame, text="", font=('Arial', 20),bg='#161625', fg='White')
    msg_label.pack()

def main_page():
    clear_sc()


    #marggg
    marg = Label(window, text="", font=('Arial', 25), fg='White', height=5, bg="#161625")
    marg.pack()
    #choice frame
    frame1 = Frame(window, width=width)
    frame1.pack()
    
    #options:
    #upload
    frame1_upload = Frame(frame1, width=400, bg="#504a63")
    frame1_upload.pack(side=LEFT)
    upload_label = Label(frame1_upload, text="Upload a File", font=('Arial', 25), fg='White', width=20, bg="#504a63")
    upload_label.pack(side=TOP)
    upload_marg = Label(frame1_upload, text="", font=('Arial', 25), fg='White', height=2, bg="#504a63")
    upload_marg.pack()
    upload_mode = Button(frame1_upload, text="Upload", font=("Arial", 25),width= 7,height=1,command=upload_page)
    upload_mode.pack()

    frame1_margin_1 = Frame(frame1, width=300,height=193, bg="#161625")
    frame1_margin_1.pack(side=LEFT)


    frame1_download = Frame(frame1, width=400, bg='#504a63')
    frame1_download.pack(side=LEFT)
    download_label = Label(frame1_download, text="Download a File", font=('Arial', 25), fg='White',width=20, bg="#504a63")
    download_label.pack()
    download_marg = Label(frame1_download, text="", font=('Arial', 25), fg='White', height=2, bg="#504a63")
    download_marg.pack()
    download_mode = Button(frame1_download, text="Download", font=("Arial", 25),width= 7,height=1,command=download_page)
    download_mode.pack()



main_page()


window.mainloop()
disconnect()