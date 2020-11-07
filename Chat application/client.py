#Program for a chat application

import socket
import os
import threading

HOST = '192.168.0.104'
PORT = 9009

sock = socket.socket()
try:
    sock.connect((HOST, PORT))
except socket.error as e:
    print(e)

def Send():
    cmd = input()
    sock.send(str.encode(cmd))
    if cmd == "quit()":
        os._exit(1)
        
def Receive():
    string = sock.recv(102400)
    string = string.decode("utf-8")
    if string == "quit()":
        os._exit(1)

    if string != "\n":
        print("\nReceived : ", string, "\n")

if __name__ == "__main__":
    while True:
        th1 = threading.Thread(target=Send)
        th2 = threading.Thread(target=Receive)

        th1.start()
        th2.start()

        th1.join()