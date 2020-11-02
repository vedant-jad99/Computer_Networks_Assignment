#Palindrome

import socket
import time

PORT = 9990
HOST = "192.168.0.105"
sock = None

def Create():
    try:
        global sock
        sock = socket.socket()
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
        if(string == 'quit()'):
            conn.send(str.encode(string))
            print("Exiting...")
            time.sleep(1)
        elif string == string[::-1]:
            conn.send(str.encode("Palindrome"))
        else:
            conn.send(str.encode("Not a palindrome"))


if __name__ == '__main__':
    Create()
    Bind()
    Listen()
    
