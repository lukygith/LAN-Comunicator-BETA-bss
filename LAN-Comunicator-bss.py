import socket
import threading

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            if message:
                print(f"Zpráva: {message}")
            else:
                break
        except:
            break

def send_messages(sock):
    while True:
        message = input("")
        sock.sendall(message.encode())
        if message.lower() == 'exit':
            break

def client_mode():
    host = input("Zadejte IP adresu serveru: ")
    port = int(input("Zadejte port serveru: "))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        print("Připojeno k serveru.")

        receive_thread = threading.Thread(target=receive_messages, args=(sock,))
        send_thread = threading.Thread(target=send_messages, args=(sock,))

        receive_thread.start()
        send_thread.start()

        receive_thread.join()
        send_thread.join()

def server_mode():
    manual = input("Chcete zadat IPv4 adresu a port ručně? (ano/ne): ").strip().lower()
    if manual == 'ano':
        host = input("Zadejte IPv4 adresu: ").strip()
        port = int(input("Zadejte port: ").strip())
    else:
        host = socket.gethostbyname(socket.gethostname())
        port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        sock.listen()
        print(f"Server naslouchá na {host}:{port}...")

        conn, addr = sock.accept()
        with conn:
            print(f"Připojeno klientem {addr}")

            receive_thread = threading.Thread(target=receive_messages, args=(conn,))
            send_thread = threading.Thread(target=send_messages, args=(conn,))

            receive_thread.start()
            send_thread.start()

            receive_thread.join()
            send_thread.join()

if __name__ == "__main__":
    mode = input("Zvolte režim (server/klient): ").strip().lower()
    if mode == 'server':
        server_mode()
    elif mode == 'klient':
        client_mode()
    else:
        print("Neplatný režim, zvolte buď 'server' nebo 'klient'.")
