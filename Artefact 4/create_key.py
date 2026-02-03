from cryptography.fernet import Fernet
k = open("key.txt","w")
key = Fernet.generate_key()
k.write(str(key)[2:-1])
k.close()