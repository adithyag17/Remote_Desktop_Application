import socket
import ssl
import zlib
from PIL import ImageGrab

# create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get server hostname and port
host = input("Enter server hostname: ")
port = int(input("Enter server port number: "))

# connect to the server
client_socket.connect((host, port))

# send username and password to server for authentication
username = input("Enter username: ")
password = input("Enter password: ")

client_socket.sendall(username.encode())
client_socket.sendall(password.encode())

# receive authentication response from server
auth_response = client_socket.recv(1024).decode()

if auth_response == "Authorization successful":
    print("Authentication successful")
else:
    print("Authentication failed")
    client_socket.close()

# create a secure SSL/TLS context
context = ssl.create_default_context()

# wrap the socket with SSL/TLS
client_socket = context.wrap_socket(client_socket, server_hostname=host)

# loop to receive screen data from server
while True:
    # receive the compressed screen data from the server
    compressed_data = client_socket.recv(4096)

    # decompress the data using zlib
    decompressed_data = zlib.decompress(compressed_data)

    # convert the data to an image and display it
    screen_image = Image.frombytes("RGB", (1920, 1080), decompressed_data)
    screen_image.show()

    # get user input
    user_input = input("Enter user input: ")

    # send user input to the server
    client_socket.sendall(user_input.encode())

    # receive a response from the server
    response = client_socket.recv(1024).decode()

    print(response)
