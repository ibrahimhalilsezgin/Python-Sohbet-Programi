#!/usr/bin/python3
import pathlib
import tkinter as tk
import tkinter.ttk as ttk
import pygubu
import socket
import threading
import json
from tkinter import messagebox
import os
import time
if not os.path.exists('cache.json'):
    with open('cache.json', 'w') as f:
        f.write('{}')


server = socket.socket()

server.connect(('localhost', 12345))

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "client.ui"
nickname_UI = PROJECT_PATH / "nickname.ui"
CACHE_FILE = PROJECT_PATH / "cache.json"

with open(CACHE_FILE) as f:
    data = json.load(f)

class Client:
    def __init__(self, master=None, translator=None):
        self.builder = builder = pygubu.Builder(translator)
        builder.add_resource_path(PROJECT_PATH)

        if "nickname" not in data:
            builder.add_from_file(nickname_UI)
            self.mainwindow = builder.get_object("frame1", master)
            self.entry = builder.get_object("entry1", master)
            builder.get_object("button1", master).config(command=self.Onay)

        else:
            builder.add_from_file(PROJECT_UI)
            # Main widget
            self.mainwindow = builder.get_object("frame1", master)
            builder.connect_callbacks(self)
            self.entry = builder.get_object("entry1", master)
            self.list = builder.get_object("listbox1", master)

    def start_receiving_messages(self):
            while True:
                try:
                    msg = server.recv(1024).decode('utf-8')
                    self.list.insert(tk.END, msg)
                    print(msg)
                except ConnectionResetError as e:
                    self.list.insert(tk.END, "Sunucuya Ulaşılamadı...")
    
    def run(self):
        self.mainwindow.mainloop()

    def send(self):
        nick = data["nickname"]
        message = f"{nick} > {self.entry.get()}"
        size = self.list.size()
        if not self.entry.get():
            messagebox.showerror('Lütfen Dolu Bir İçerik Giriniz...')
            pass
        print(size)
        self.list.insert(size, message)
        server.sendall(message.encode('utf-8'))

        self.entry.delete(0, tk.END)

    def Onay(self):
        nickname = self.entry.get()
        if len(nickname) == 0:
            messagebox.showerror("hata", "Lütfen Geçerli Bir İsim Girin...")
            return
        messagebox.showinfo(
        "Basarili",
        "İsminiz Basariyla ayarlandi. simdi programı tekrar baslatin")
        data["nickname"] = nickname
        with open(CACHE_FILE, "w") as f:
            json.dump(data, f)
        exit()

if __name__ == "__main__":
    root = tk.Tk()
    app = Client(root)
    thread = threading.Thread(target=app.start_receiving_messages, daemon=True)
    thread.start()

    app.run()
