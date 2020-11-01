#Program to capitalise the string

import socket
import sys

HOST = '192.168.0.105'
PORT = 8080

sock = socket.socket()
try:
    sock.connect((HOST, PORT))
    print("List of viable commands is: list(), select(), quit().")
except socket.error as e:
    print(e)

commands = ['select()', 'list()', 'quit()']

while True:
    cmd = input()
    if cmd in commands:
        sock.send(str.encode(cmd))
        if cmd == 'list()':
            while True:
                recv = sock.recv(1024)
                recv = recv.decode("utf-8")
                if 'over' in recv:
                    break
                print(recv)
        elif cmd == 'quit()':
            break
