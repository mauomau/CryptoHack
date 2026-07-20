import hashlib
from pwn import log

# --- PARAMÈTRES DE LA COURBE E(Fp) ---
a = 497
b = 1768
p = 9739

# --- DONNÉES DU DÉFI ---
QA = (815, 3190)  # Clé publique d'Alice
nB = 1829         # Ta clé privée (Bob)

# --- 1. FONCTIONS DE BASE DE LA COURBE ---
def add_points(P1, P2, a, p):
    if P1 is None: return P2
    if P2 is None: return P1
    
    x1, y1 = P1
    x2, y2 = P2
    
    if x1 == x2 and (y1 == -y2 % p):
        return None
        
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
        if n % 2 == 1:
            R = add_points(R, Q, a, p)
        Q = add_points(Q, Q, a, p)
        n = n // 2
    return R

# --- 2. CALCUL DU SECRET PARTAGÉ ---
# S = [nB]QA
S = double_and_add(QA, nB, a, p)
log.info(f"Point secret partagé S calculé : {S}")

# --- 3. VÉRIFICATION D'APPARTENANCE A LA COURBE ---
x_s, y_s = S
lhs = pow(y_s, 2, p)
rhs = (pow(x_s, 3, p) + a * x_s + b) % p
assert lhs == rhs, "Le point calculé n'est pas sur la courbe !"

# --- 4. DÉRIVATION DE LA CLÉ (SHA-1) ---
# "take the integer representation of the coordinate and cast it to a string"
shared_x_str = str(x_s)

# Calcul du hash SHA-1
sha1_hash = hashlib.sha1(shared_x_str.encode()).hexdigest()

log.success("Vérification de la courbe réussie.")
print(f"[★] FLAG : {sha1_hash}")