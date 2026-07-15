from Crypto.Hash import SHA256
from Crypto.Util.number import bytes_to_long

def solve():
    # 1. Charger les paramètres RSA N et d depuis le fichier
    with open("Public-Key Cryptography/private_0a1880d1fffce9403686130a1f932b10.key", "r") as f:
        lines = f.readlines()
    
    N = int(lines[0].split("=")[1].strip())
    d = int(lines[1].split("=")[1].strip())
        
    # Le message (flag) à signer fourni par l'énoncé
    msg = b"crypto{Immut4ble_m3ssag1ng}"
    
    # 2. Calculer le hash SHA256 du message
    h = SHA256.new(msg)
    hash_bytes = h.digest()

    
    # 3. Convertir les octets du hash en un grand entier
    hash_as_long = bytes_to_long(hash_bytes)
    
    # 4. Calculer la signature RSA : S = H(m)^d mod N
    signature = pow(hash_as_long, d, N)
    
    print("Voici le nombre à soumettre sur CryptoHack :")
    print(signature)

if __name__ == "__main__":
    solve()