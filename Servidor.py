import socket
import threading
import random

Host = "192.168.86.3"
Port = 12511

Palavras = random.choice([x for x in open("./Palavras.txt").readlines()]).replace("\n","")
Palavra = [letra for letra in Palavras]
Formando = []
for nada in Palavras:
    Formando.insert(Palavra.index(nada),"")

Tentativas = 5

Clientes = []
Nicks = []
Banido = []

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((Host,Port))
s.listen()

def Mandar(Mensagem):
    for Cliente in Clientes:
        try:
            Cliente.send(Mensagem)
        except:
            Mandar(f"O Jogador {Nicks[Clientes.index(Cliente)]} saiu do jogo".encode("utf-8"))
            print(f"O Jogador {Nicks[Clientes.index(Cliente)]} saiu do jogo")
            Cliente.close()

def Expulsar(Nick):
    global Nicks
    Sla = Nicks
    C = Clientes[Sla.index(Nick)]
    C.close()

def Jogo(Cliente,Msg):
    global Palavra,Palavras,Formando,Tentativas
    Chute = Msg.decode("utf-8").split(" ")[1]
    if("kick" in Chute):
        Expulsar(Msg.decode("utf-8").split("kick ")[1])
    else:
        if(Chute in Palavra):
            try:
                for x in range(len(Palavras)):
                    Formando[Palavra.index(Chute,x,len(Palavras))] = Chute
            except:
                pass
            finally:
                for Cliente in Clientes:
                    Cliente.send(str(Formando).encode("utf-8"))
            if(Formando == Palavra):
                for Cliente in Clientes:
                    Cliente.send("Acertaram todas as letras\n".encode("utf-8"))
                    Cliente.send("Recomeçando o jogo...\n".encode("utf-8"))
                Palavras = random.choice([x for x in open("./Palavras.txt").readlines()]).replace("\n","")
                Palavra = [letra for letra in Palavras]
                Formando = []
                for nada in Palavras:
                    Formando.insert(Palavra.index(nada),"")
                Tentativas = 5
                Mandar("Jogo Pronto\n".encode("utf-8"))
                Mandar(str(Formando).encode("utf-8"))
            if(Chute in Palavra):
                Mandar("Acertaram uma letra\n".encode("utf-8"))
                Mandar(str(Formando).encode("utf-8"))
        else:    
            Tentativas-=1
            Tentar = Tentativas
            Mandar(f"Erraram uma letra mais voces ainda tem {Tentar} Tentativas!!".encode("utf-8"))
        if(Tentativas==0):
            Mandar(f"Voces perderam, o jogo esta recomeçando...\n".encode("utf-8"))
            Palavras = random.choice([x for x in open("./Palavras.txt").readlines()]).replace("\n","")
            Palavra = [letra for letra in Palavras]
            Formando = []
            for nada in Palavras:
                Formando.insert(Palavra.index(nada),"")
            Tentativas = 5
            Mandar(f"Jogo Pronto\n")
            Mandar(str(Formando).encode("utf-8"))

def Receber(Cliente):
    while True:
        try:
            Msg = Cliente.recv(1024)
            Jogo(Cliente,Msg)
        except Exception:
            break

def Start():
    global Formando
    while True:
        Conn,Adress = s.accept()
        if(Conn in Banido):
            Conn.close()
        else:
            Clientes.append(Conn)
            Nick = Conn.recv(1024).decode("utf-8")
            Nicks.append(Nick)
            Conn.send(str(Formando).encode("utf-8"))
            print(f"Um Jogador logou usando o Ip{Adress} e o Nick({Nick})")
            Mandar(f"Um jogador entrou na sala com o nick {Nick}".encode("utf-8"))
            ReceberThread = threading.Thread(target=Receber,args=(Conn,))
            ReceberThread.start()


print("Servidor Ativado")
Start()