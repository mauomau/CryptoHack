from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib

# --- 1. DONNÉES DU DÉFI ---
p = 1331169830894825846283645180581
a = -35
b = 98

E = EllipticCurve(GF(p), [a, b])
G = E(479691812266187139164535778017, 568535594075310466177352868412)
P1 = E(1110072782478160369250829345256, 800079550745409318906383650948)
P2 = E(1290982289093010194550717223760, 762857612860564354370535420319)

N = G.order()

# --- 2. ATTAQUE MOV EXPLICITE ---
print("[+] Extension vers le corps F_(p^2)...")
K.<a> = GF(p**2)
EK = E.change_ring(K)

GK = EK(G)
P1K = EK(P1)
P2K = EK(P2)

# Recherche d'un point auxiliaire R sur EK
print("[+] Recherche d'un point auxiliaire R...")
while True:
    R = EK.random_point()
    R = (R.order() // N) * R
    if R != EK(0) and GK.weil_pairing(R, N) != 1:
        break

# Calcul des accouplements de Weil (u et v dans F_(p^2)*)
u = GK.weil_pairing(R, N)
v = P1K.weil_pairing(R, N)

# Résolution du logarithme discret dans F_(p^2)* (Ultra rapide !)
print("[+] Résolution du DLP dans F_(p^2)...")
n_a = v.log(u)
print(f"[✓] Clé privée d'Alice n_a = {n_a}")

# --- 3. CALCUL DU SECRET ET DÉCHIFFREMENT ---
S = n_a * P2
shared_secret_x = int(S[0])

iv = bytes.fromhex('eac58c26203c04f68d63dc2c58d79aca')
ciphertext = bytes.fromhex('bb9ecbd3662d0671fd222ccb07e27b5500f304e3621a6f8e9c815bc8e4e6ee6ebc718ce9ca115cb4e41acb90dbcabb0d')

sha1 = hashlib.sha1()
sha1.update(str(shared_secret_x).encode('ascii'))
key = sha1.digest()[:16]

cipher = AES.new(key, AES.MODE_CBC, iv)
plaintext = unpad(cipher.decrypt(ciphertext), 16)
print(f"\n[★] FLAG : {plaintext.decode('ascii')}")