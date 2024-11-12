from py_redis.server_socket import accept_client
import socket

target_host = "0.0.0.0"
target_port = 9999


accept_client(target_host, target_port)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_host, target_port))
client.send("Hello. Signed: The client".encode())
response = client.recv(4096)
print(response.decode())
