## Cryptograhic functions used for CryptoChat
from cryptography.hazmat.primitives.asymmetric import ec # imports Elliptic Curve module ('SECP3841()')
from cryptography.hazmat.backends import default_backend # Runs the EC math "behind the scenes"
from cryptography.hazmat.primitives import serialization # Allows for serialization of keys to bits

def generateKeyPair():
  privateKey = ec.generate_private_key(ec.SECP384R1, default_backend) # uses the SECP384R1 elliptic curve points and default backend to calculate private keys
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


