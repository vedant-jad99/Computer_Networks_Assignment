#Program to return square and cube of number

import socket
import re

HOST = '192.168.0.105'
PORT = 9999
p = re.compile('[a-zA-Z]+')

sock = socket.socket()
sock.connect((HOST, PORT))

new_string = ""
while new_string.lower() != 'quit()':
    string = input()
    words = p.findall(string)
    if words != []:
        if 'quit' in words:
            new_string = "quit()"
            sock.send(str.encode(string.strip()))        
            continue
        print("\nValueError: Enter an integer\n")
        continue
    sock.send(str.encode(string.strip()))
    new_string = sock.recv(1024)
    new_string = new_string.decode("utf-8")
    print('\nReceived : ', new_string, '\n')