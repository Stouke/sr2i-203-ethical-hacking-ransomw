import os
from cryptography.fernet import Fernet


files=[]

for file in os.listdir():
    if file == "decrypt_ransomware.py" or file =="encrypt_ransomware.py" or file=="PrivateKey.key":
        continue
    if os.path.isfile(file):
        files.append(file)

print(files)

with open("PrivateKey.key", "rb") as thekey:
    secretkey= thekey.read()

for file in files:
    with open(file, "rb") as thefile:
        contents= thefile.read()
    contents_decrypted = Fernet(secretkey).decrypt(contents)
    with open(file,"wb") as thefile:
        thefile.write(contents_decrypted)