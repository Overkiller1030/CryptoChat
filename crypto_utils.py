## Cryptograhic functions used for CryptoChat 
from cryptography.hazmat.primitives.asymmetric import ec # imports Elliptic Curve module ('SECP3841()')
from cryptography.hazmat.backends import default_backend # Runs the EC math "behind the scenes"
from cryptography.hazmat.primitives import serialization # Allows for serialization of keys to bits
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes # AES-GCM encryption/decryption
from cryptography.hazmat.primitives.kdf.hkdf import HKDF # Creates encryption key that fits AES-requirements from shared secret (This is HMAC)
from cryptography.hazmat.primitives import hashes # Used with HKDF
from cryptography.hazmat.primitives import padding # Padding to fit AES-block size
import os



def generateKeyPair():
  privateKey = ec.generate_private_key(ec.SECP384R1(), default_backend) # uses the SECP384R1 elliptic curve points and default backend to calculate private keys
  publicKey = privateKey.public_key() # Creates public key from generated private key
  return privateKey, publicKey

## Instead of emailing public keys like in class, we serialize it to bits, sending it through the network to other user (Think WireShark)

def serializePublicKey(publicKey):
  return publicKey.public_bytes(
    encoding=serialization.Encoding.PEM, ## Makes keys-turned-bytes readable to humans (PEM)
    format = serialization.PublicFormat.SubjectPublicKeyInfo ## Makes keys-turned-bytes readable to CryptoChat
  )

def deserializePublicKey(PublicKeyBytes):
  return serialization.load_pem_public_key(PublicKeyBytes, backend=default_backend()) ## Reads PEM Key-To-Bytes Public Key and converts it back to regular object

## Now that users have public/private key, we use Diffie-Hellman

def getSharedSecret(myPrivateKey, recieverPublicKey):
  sharedSecret = myPrivateKey.exchange(ec.ECDH(), recieverPublicKey) # Uses my private key, reciever public key, and Diffie-Hellman to create a shared secret
  return sharedSecret


## We need to turn the shared secret from Diffie-Hellman into an AES-256 bit key

def encryptMessage(sharedSecret, plaintext):
  key = HKDF(
    algorithm = hashes.SHA256(), # HKDF uses SHA256 to make the key
    length = 32, # 32 bytes = 256 bits
    salt = None, # Salt ensures keys are unique. Because we've used Diffie-Hellman, they are already unique, and we don't need salt
    info = b'key exchange CryptoChat', # Explanation for making a key
    backend = default_backend() # What we use to calculate the key
  ).derive(sharedSecret) # Uses all this information to turn shared secret into a 256-bit secure key

  iv = os.urandom(12) # Creates a random 12 byte IV for AES-GCM

## Now that the key is correct, we need to use the key and iv for AES_GCM and encrypt the plaintext

  encryptor = Cipher(
    algorithms.AES(key),
    modes.GCM(iv),
    backend=default_backend()
  ).encryptor()

  ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
  
  return iv, ciphertext, encryptor.tag

## This is used for decryption. Same key is generated because shared secret is same for both users

def decryptMessage(sharedSecret, iv, ciphertext, tag):
  key = HKDF(
    algorithm = hashes.SHA256(), # HKDF uses SHA256 to make the key
    length = 32, # 32 bytes = 256 bits
    salt = None, # Salt ensures keys are unique. Because we've used Diffie-Hellman, they are already unique, and we don't need salt
    info = b'key exchange CryptoChat', # Explanation for making a key
    backend = default_backend() # What we use to calculate the key
  ).derive(sharedSecret) # Uses all this information to turn shared secret into a 256-bit secure key

  decryptor = Cipher(
    algorithms.AES(key),
    modes.GCM(iv, tag),
    backend=default_backend()
  ).decryptor()

  plaintext = decryptor.update(ciphertext) + decryptor.finalize()

  return plaintext.decode()