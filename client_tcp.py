import socket
# The param AF_INET indicates that we are using IP protocol
# The param SOCKET_STREAM defines using TCP protocol
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect(("127.0.0.1", 8820))
# encode translate the str to binary
my_socket.send("hello".encode())
# the param in the recv method defines the max bytes we want to extract from the socket
# decode method translate the binary sequence to string
data = my_socket.recv(1024).decode()
print("The server sent" + data)
my_socket.close()
