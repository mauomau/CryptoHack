import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from pwn import log

# --- PARAMÈTRES DE LA COURBE ---
a = 497
b = 1768
p = 9739

# --- DONNÉES DU DÉFI ---
x_QA = 4726
nB = 6534
iv_hex = 'cd9da9f1c60925922377ea952afc212c'
ciphertext_hex = 'febcbe3a3414a730b125931dccf912d2239f3e969c4334d95ed0ec86f6449ad8'

# --- 1. RECONSTRUCTION DE LA COORDONNÉE Y ---
# Étape A: Calcul de y^2
y_square = (pow(x_QA, 3, p) + a * x_QA + b) % p

# Étape B: Racine carrée modulaire car p = 3 mod 4 (9739 % 4 == 3)
exp = (p + 1) // 4
y_QA = pow(y_square, exp, p)

QA = (x_QA, y_QA)
log.info(f"Point public d'Alice reconstruit : QA = {QA}")

# --- 2. FONCTIONS DE LA COURBE ---
def add_points(P1, P2, a, p):
    if P1 is None: return P2
    if P2 is None: return P1
    x1, y1 = P1
    x2, y2 = P2
    if x1 == x2 and (y1 == -y2 % p): return None
    if P1 != P2:
        num = (y2 - y1) % p
        denom = (x2 - x1) % p
        lamb = (num * pow(denom, -1, p)) % p
    else:
        if y1 == 0: return None
        num = (3 * pow(x1, 2, p) + a) % p
        denom = (2 * y1) % p
        lamb = (num * pow(denom, -1, p)) % p
    x3 = (pow(lamb, 2, p) - x1 - x2) % p
    y3 = (lamb * (x1 - x3) - y1) % p
    return (x3, y3)

def double_and_add(P, n, a, p):
    Q = P
    R = None
    while n > 0:
        if n % 2 == 1: R = add_points(R, Q, a, p)
        Q = add_points(Q, Q, a, p)
        n = n // 2
    return R

# --- 3. CALCUL DU SECRET PARTAGÉ ---
S = double_and_add(QA, nB, a, p)
shared_secret_x = S[0]
log.success(f"Coordonnée X du secret partagé trouvée : {shared_secret_x}")

# --- 4. DÉCHIFFREMENT DU FLAG (Code CryptoHack fourni) ---
def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))

def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode('ascii')

flag = decrypt_flag(shared_secret_x, iv_hex, ciphertext_hex)
print(f"\n[★] FLAG : {flag}")