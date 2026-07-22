import hashlib
import json
from pwn import remote
from Crypto.Util.number import bytes_to_long
from ecdsa.ecdsa import generator_192

# Paramètres de la courbe NIST P-192
g = generator_192
n_curve = g.order()

def sha1(data):
    sha1_hash = hashlib.sha1()
    sha1_hash.update(data)
    return sha1_hash.digest()

# 1. Connexion au serveur
io = remote("socket.cryptohack.org", 13381)
io.recvuntil(b"verify.\n")

# 2. Demande d'une signature temporelle
io.sendline(json.dumps({"option": "sign_time"}).encode())
resp = json.loads(io.recvline().decode())

msg = resp["msg"]
r = int(resp["r"], 16)
s = int(resp["s"], 16)
h = bytes_to_long(sha1(msg.encode()))

# 3. Brute-force du petit nonce k (1 <= k < 60)
k_found = None
for k_cand in range(1, 60):
    P = g * k_cand
    if P.x() % n_curve == r:
        k_found = k_cand
        break

print(f"[+] Nonce k trouvé : {k_found}")

# 4. Calcul de la clé privée d
r_inv = pow(r, -1, n_curve)
d = (r_inv * (s * k_found - h)) % n_curve
print(f"[+] Clé privée d extraite : {d}")

# 5. Signature forgée pour le message "unlock"
msg_target = "unlock"
h_target = bytes_to_long(sha1(msg_target.encode()))

# Nonce k arbitraire mais valide
k_target = 1337
r_target = (g * k_target).x() % n_curve
k_target_inv = pow(k_target, -1, n_curve)
s_target = (k_target_inv * (h_target + d * r_target)) % n_curve

# 6. Envoi au serveur pour obtenir le flag
verify_payload = {
    "option": "verify",
    "msg": msg_target,
    "r": hex(r_target),
    "s": hex(s_target)
}
io.sendline(json.dumps(verify_payload).encode())
print(f"[★] Réponse : {io.recvline().decode().strip()}")