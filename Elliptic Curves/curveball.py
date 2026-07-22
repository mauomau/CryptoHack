import json
from pwn import remote, log
from fastecdsa.curve import P256
from fastecdsa.point import Point

# --- 1. COORDONNÉES DE BING (Tirées de 13382.py) ---
bing_pk = Point(
    0x3B827FF5E8EA151E6E51F8D0ABF08D90F571914A595891F9998A5BD49DFA3531, 
    0xAB61705C502CA0F7AA127DEC096B2BBDC9BD3B4281808B3740C320810888592A, 
    curve=P256
)

# --- 2. CALCUL DU FAUX GÉNÉRATEUR ---
# On choisit d = 2 (car d = 1 est interdit)
d_fake = 2

# Ordre de la courbe P256
order = P256.q

# Calcul de l'inverse de d_fake mod order
d_inv = pow(d_fake, -1, order)

# Notre faux générateur g = Q_bing * d_inv
g_fake = bing_pk * d_inv

log.info(f"Faux générateur calculé :")
log.info(f"x: {hex(g_fake.x)}")
log.info(f"y: {hex(g_fake.y)}")

# --- 3. ENVOI DU PAYLOAD ---
payload = {
    "private_key": d_fake,
    "host": "www.bing.com",
    "curve": "secp256r1",
    "generator": [g_fake.x, g_fake.y]
}

# Connexion au serveur de CryptoHack
io = remote("socket.cryptohack.org", 13382)
io.recvuntil(b"library!\n")

# Envoi du JSON
log.info("Envoi du faux certificat pour usurper www.bing.com...")
io.sendline(json.dumps(payload).encode())

# Récupération de la réponse contenant le flag
response = io.recvline().decode().strip()
log.success(f"Réponse du serveur : {response}")