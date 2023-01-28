from Crypto.PublicKey import RSA

key= RSA.generate(2048)
privateKey= key.export_key()
publicKey= key.publickey().export_key() ## On peut pas retrouver la clé à partir de ça?

# save private key to file

with open("private.pem", "wb") as file:
    file.write(privateKey)

# Sauvegarder la clé public dans le fichier

with open("public.pem", "wb") as file:
    file.write(publicKey)

print("La clé publique a été sauvegardé dans private.pem")
print('Public key saved to public.pem')
