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
    while True:
        cmd = input()
        sock.send(str.encode(cmd))
        if cmd == "quit()":
            os._exit(1)
        
def Receive():
    while True:
        string = sock.recv(102400)
        string = string.decode("utf-8")
        if string == "quit()":
            sock.send(str.encode(string))
            sock.close()
            os._exit(1)

        if string != "\n":
            print("\nReceived : ", string, "\n")

if __name__ == "__main__":
    th1 = threading.Thread(target=Send)
    th2 = threading.Thread(target=Receive)
    th1.start()
    th2.start()

    th1.join()