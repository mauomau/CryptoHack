from pwn import log

# --- PARAMÈTRES DE LA COURBE ---
# E: Y^2 = X^3 + aX + b mod p
a = 497
b = 1768
p = 9739

# Points donnés par l'énoncé
P = (493, 5564)
Q = (1539, 4742)
R = (4403, 5202)

def add_points(P1, P2, a, p):
    """
    Implémente l'algorithme d'addition de deux points sur une courbe de Weierstrass
    Retourne None pour représenter le point à l'infini (O).
    """
    # Cas (a) et (b) : Gestion de l'élément neutre (O)
    if P1 is None: return P2
    if P2 is None: return P1
    
    x1, y1 = P1
    x2, y2 = P2
    
    # Cas (d) : P + (-P) = O
    if x1 == x2 and (y1 == -y2 % p):
        return None
        
    # Cas (e1) : Addition de deux points distincts (P != Q)
    if P1 != P2:
        num = (y2 - y1) % p
        denom = (x2 - x1) % p
        # Utilisation de pow(denom, -1, p) pour l'inverse modulaire
        lamb = (num * pow(denom, -1, p)) % p
        
    # Cas (e2) : Doublement d'un point (P == Q)
    else:
        num = (3 * pow(x1, 2, p) + a) % p
        denom = (2 * y1) % p
        lamb = (num * pow(denom, -1, p)) % p
        
    # Calcul des coordonnées de destination (f, h, i)
    x3 = (pow(lamb, 2, p) - x1 - x2) % p
    y3 = (lamb * (x1 - x3) - y1) % p
    
    return (x3, y3)

# --- VÉRIFICATION DES CAS DE TEST ---
X = (5274, 2841)
Y = (8669, 740)
assert add_points(X, Y, a, p) == (1024, 4440), "Erreur de test sur X + Y"
assert add_points(X, X, a, p) == (7284, 2107), "Erreur de test sur X + X"
log.success("Algorithme validé sur les cas de test CryptoHack !")

# --- CALCUL DE S = P + P + Q + R ---
# Étape 1 : 2P = P + P
double_P = add_points(P, P, a, p)

# Étape 2 : 2P + Q
double_P_plus_Q = add_points(double_P, Q, a, p)

# Étape 3 : (2P + Q) + R
S = add_points(double_P_plus_Q, R, a, p)

log.info(f"Coordonnées trouvées pour S : {S}")

# --- VÉRIFICATION D'APPARTENANCE À LA COURBE ---
x_s, y_s = S
lhs = pow(y_s, 2, p)
rhs = (pow(x_s, 3, p) + a * x_s + b) % p

if lhs == rhs:
    log.success("Validation mathématique : Le point S appartient bien à la courbe E(Fp).")
    print(f"\n[★] FLAG : crypto{{{x_s},{y_s}}}")
else:
    log.failure("Le point calculé n'est pas sur la courbe. Vérifie les inversions modulaires.")