import socket
import threading

Host = "192.168.86.3"
Port = 12511

Nick = input("Digite seu Nick\n>")

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((Host,Port))
s.send(Nick.encode("utf-8"))

def Receber():
    while True:
        print(s.recv(1024).decode("utf-8"))

def Enviar():
    while True:
        Mensagem = input("")
        s.send(f"{Nick}> {Mensagem}".encode("utf-8"))

ReceberThread = threading.Thread(target=Receber)
EnviarThread = threading.Thread(target=Enviar)
ReceberThread.start()
EnviarThread.start()