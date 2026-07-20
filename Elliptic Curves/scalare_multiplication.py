from pwn import log

# Paramètres de la courbe E: Y^2 = X^3 + 497X + 1768 mod 9739
a = 497
b = 1768
p = 9739

# --- OUTIL : ADDITION / DOUBLEMENT DE POINTS ---
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
        if y1 == 0:
            return None
        num = (3 * pow(x1, 2, p) + a) % p
        denom = (2 * y1) % p
        lamb = (num * pow(denom, -1, p)) % p
        
    x3 = (pow(lamb, 2, p) - x1 - x2) % p
    y3 = (lamb * (x1 - x3) - y1) % p
    
    return (x3, y3)

# --- LE MOTEUR : DOUBLE AND ADD ---
def double_and_add(P, n, a, p):
    """
    Calcule Q = [n]P en complexité O(log n)
    """
    Q = P
    R = None  # Représente le Point à l'infini (O)
    
    while n > 0:
        if n % 2 == 1:
            R = add_points(R, Q, a, p)
        Q = add_points(Q, Q, a, p) # Doublement
        n = n // 2                 # Division entière par 2
        
    return R

# --- TEST DE L'ALGORITHME ---
X = (5323, 5438)
test_res = double_and_add(X, 1337, a, p)
assert test_res == (1089, 6931), f"Erreur de test, obtenu: {test_res}"
log.success("Algorithme de multiplication scalaire validé par le test !")

# --- DÉFI REEL ---
P = (2339, 2213)
scalar = 7863

Q = double_and_add(P, scalar, a, p)
log.info(f"Point résultant [7863]P : {Q}")

# --- VÉRIFICATION D'APPARTENANCE ---
x_q, y_q = Q
lhs = pow(y_q, 2, p)
rhs = (pow(x_q, 3, p) + a * x_q + b) % p

if lhs == rhs:
    log.success("Validation : Le point Q appartient bien à la courbe E(Fp) !")
    print(f"\n[★] FLAG : crypto{{{x_q},{y_q}}}")
else:
    log.failure("Le point calculé n'est pas sur la courbe.")