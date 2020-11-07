#Chat Application

import socket
import time
import threading
import os

PORT = 9009
HOST = '192.168.0.104'
sock = None
loopExit = True

def Create():
    try:
        global sock
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except:
        print("Error creating socket")

def Bind():
    try:
        global sock
        print("Binding the port...")
        sock.bind((HOST, PORT))
        sock.listen(5)
    except socket.error as e:
        print(e)
        Bind()
    
def Listen():
    try:
        conn, addr = sock.accept()
        if conn != None:
            print("Connection to server successful.\n")
        
        th1 = threading.Thread(target=Receive, args=(conn, ))
        th2 = threading.Thread(target=Send, args=(conn, ))
        th1.start()
        th2.start()

        th1.join()
   
    except socket.error as e:
        print(e)

def Send(conn):
    while True:
        cmd = input()
        conn.send(str.encode(cmd))
        if cmd == "quit()":
            time.sleep(1)
            os._exit(1)

def Receive(conn):
    while True:
        string = conn.recv(102400)
        string = string.decode("utf-8")
        print("\nReceived : ", string, "\n")
        if(string == 'quit()'):
            conn.send(str.encode(string))
            print("Exiting...")
            conn.close()
            time.sleep(1)
            os._exit(1)

if __name__ == '__main__':
    Create()
    Bind()
    Listen()
    
