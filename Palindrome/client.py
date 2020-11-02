#Program to find string is palindrome or not

import socket
import sys

HOST = '192.168.0.105'
PORT = 9990

sock = socket.socket()
sock.connect((HOST, PORT))

new_string = ""
while new_string.lower() != 'quit()':
    string = input()
    sock.send(str.encode(string))
    new_string = sock.recv(1024)
    new_string = new_string.decode("utf-8")
    if 'quit' in new_string:
        continue
    print('\nReceived : ', new_string, '\n')