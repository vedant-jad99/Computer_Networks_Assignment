#Capitalise

import socket
import time

PORT = 9000
HOST = '192.168.43.252'
sock = None

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
            print("Connection to server successful. \nIn this application, you can send a strign and we will return a \ncapitalised version of that string.\nFor closing the connection enter quit().\n")
        Receive(conn)
        conn.close()
    except socket.error as e:
        print(e)

def Receive(conn):
    string = ""
    while string != 'quit()':
        string = str(conn.recv(1024), "utf-8")
        print("Received : ", string)
        conn.send(str.encode(string.upper()))
        if(string == 'quit()'):
            print("Exiting...")
            time.sleep(1)

if __name__ == '__main__':
    Create()
    Bind()
    Listen()
    
