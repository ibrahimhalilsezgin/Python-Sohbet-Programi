import socket
import threading

HOST = 'localhost' # Sadece Localde çalıştırmak isterseniz localhost yazabilirsiniz ...
PORT = 12345


clients = {}

def client(client_socket, client_addr):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"({client_addr}): {message}")
            for addr, soket in clients.items():
                if soket != client_socket:
                    if not message:
                        pass
                    else:
                        soket.send(f"{message}".encode('utf-8'))
        except ConnectionResetError:
            break

    client_socket.close()
    del clients[client_addr]
    print(f"Bir bağlantı kesildi: {client_addr}")
def starttheserver():
    server_socket = socket.socket()
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Sunucu Aktif: {HOST}:{PORT}")
    while True:
        client_socket, client_addr = server_socket.accept()
        clients[client_addr] = client_socket
        thread = threading.Thread(target=client, args=(client_socket, client_addr))
        thread.start()
        print(f"Bir Kullanıcı Bağlandı {client_addr}")

starttheserver()
