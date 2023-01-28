from cryptography.fernet import Fernet
import socket

#Generation de la clé et on l'affiche
key= Fernet.generate_key()
print("Your key is:", key)

#On crée la socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 4321))
s.listen()

conn, addr= s.accept()
print(addr, "connected")

#Quand on reçoit la "key",on envoie la clé
msg= conn.recv(2048).decode()

if msg == "key": 
    conn.send(key)
    print("Key send !")
    