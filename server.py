import threading
import streamlit as st
import socket
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode

host = ''
port = 9999
server = socket.socket()
server.bind((host, port))
server.listen()
clients = []
aliases = []

def encrypt_data(plain_text):
    # Generate a 16-byte (128-bit) key and initialization vector (IV)
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CFB)
    iv = cipher.iv  # initialization vector

    # Encrypt the plain text
    cipher_text = cipher.encrypt(plain_text.encode('utf-8'))

    # Encode the key, IV, and ciphertext in Base64 for easy transmission
    encrypted_data = b64encode(key + iv + cipher_text).decode('utf-8')
    return encrypted_data
print(f"Pass Key is : {encrypt_data(socket.gethostbyname(socket.gethostname()))}")

def broadcast(message):
    for client in clients:
        client.send(message)
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat room!'.encode('utf-8'))
            aliases.remove(alias)
            break
def receive():
    while True:
        print('Server is running and listening ...')
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        # client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)
        print(f'The alias of this client is {alias}'.encode('utf-8'))
        broadcast(f'{alias.decode()} has connected to the chat room'.encode('utf-8'))
        client.send('you are now connected!'.encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    receive()