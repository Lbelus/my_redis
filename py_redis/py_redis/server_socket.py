import socket 
import threading 

bind_ip = "0.0.0.0" 
bind_port = 9999


def set_socket(bind_ip, bind_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server.bind((bind_ip, bind_port)) 
    server.listen(5) 
    print(f"[+] Listening on port {bind_ip} : {bind_port}")                            

def handle_client(client_socket): 
    request = client_socket.recv(1024) 
    print(f"[+] Recieved: {request}") 
    client_socket.send("Ping recevied".encode()) 
    client_socket.close()


def accept_client(bind_ip, bind_port):
    set_socket(bind_ip, bind_port)
    while True: 
        client, addr = server.accept() 
        print(f"[+] Accepted connection from: {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start() 
