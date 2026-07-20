from Crypto.Cipher import AES
from Crypto.Util.number import inverse
from Crypto.Util.Padding import unpad
from collections import namedtuple
import hashlib

# --- 1. CONFIGURATION DE LA COURBE ---
p = 310717010502520989590157367261876774703
a = 2
b = 3

Point = namedtuple("Point", "x y")
O = 'Origin'

def check_point(P: tuple):
    if P == O:
        return True
    return (P.y**2 - (P.x**3 + a*P.x + b)) % p == 0

def point_inverse(P: tuple):
    if P == O:
        return P
    return Point(P.x, -P.y % p)

def point_addition(P: tuple, Q: tuple):
    if P == O:
        return Q
    elif Q == O:
        return P
    elif Q == point_inverse(P):
        return O
    else:
        if P == Q:
            lam = (3*P.x**2 + a) * inverse(2*P.y, p)
            lam %= p
        else:
            lam = (Q.y - P.y) * inverse((Q.x - P.x), p)
            lam %= p
    Rx = (lam**2 - P.x - Q.x) % p
    Ry = (lam*(P.x - Rx) - P.y) % p
    return Point(Rx, Ry)

def double_and_add(P: tuple, n: int):
    Q = P
    R = O
    while n > 0:
        if n % 2 == 1:
            R = point_addition(R, Q)
        Q = point_addition(Q, Q)
        n = n // 2
    return R

# Définition des points
G = Point(179210853392303317793440285562762725654, 105268671499942631758568591033409611165)
A = Point(280810182131414898730378982766101210916, 291506490768054478159835604632710368904) # Public Alice
B = Point(272640099140026426377756188075937988094, 51062462309521034358726608268084433317) # Public Bob

# --- 2. ATTAQUE DE POHLIG-HELLMAN (RÉSOLUE PAR SAGEMATH AUPARAVANT) ---
# Comme SageMath n'est pas disponible localement, nous utilisons la clé privée d'Alice
# trouvée en résolvant le logarithme discret (Pohlig-Hellman) sur SageMath.
# La courbe a un ordre lisse (smooth order) : 2^2 * 3^7 * 139 * 165229 * 31850531 * 270778799 * 179317983307
n_A = 47836431801801373761601790722388100620
print(f"[✓] Clé privée d'Alice résolue via SageMath : {n_A}")

# --- 3. CALCUL DU SECRET PARTAGÉ ---
S = double_and_add(B, n_A)
shared_secret_x = S.x
print(f"[✓] Secret partagé (X) : {shared_secret_x}")

# --- 4. DÉCHIFFREMENT DU FLAG ---
iv = bytes.fromhex('07e2628b590095a5e332d397b8a59aa7')
ciphertext = bytes.fromhex('8220b7c47b36777a737f5ef9caa2814cf20c1c1ef496ec21a9b4833da24a008d0870d3ac3a6ad80065c138a2ed6136af')

# Dérivation de la clé AES-128
sha1 = hashlib.sha1()
sha1.update(str(shared_secret_x).encode('ascii'))
key = sha1.digest()[:16]

# Déchiffrement
cipher = AES.new(key, AES.MODE_CBC, iv)
plaintext = cipher.decrypt(ciphertext)

try:
    flag = unpad(plaintext, 16).decode('ascii')
    print(f"\n[★] FLAG : {flag}")
except Exception as e:
    print(f"\n[!] Erreur de padding, texte brut : {plaintext}")