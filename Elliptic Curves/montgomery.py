import sys

# --- PARAMÈTRES DE LA COURBE (Curve25519) ---
A = 486662
B = 1
p = 2**255 - 19

# --- DONNÉES DU DÉFI ---
x_G = 9
k = 0x1337c0decafe

# --- 1. ALGORITHME DE TONELLI-SHANKS (Pour trouver G.y) ---
def modular_sqrt(a, p):
    if pow(a, (p - 1) // 2, p) != 1:
        return None  # Pas de racine carrée
    if p % 4 == 3:
        return pow(a, (p + 1) // 4, p)
    
    # Décomposition de p-1
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    
    # Trouver un non-résidu z
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1
        
    m = s
    c = pow(z, q, p)
    t = pow(a, q, p)
    r = pow(a, (q + 1) // 2, p)
    
    while t != 1:
        t2i = t
        i = 0
        for i in range(1, m):
            t2i = pow(t2i, 2, p)
            if t2i == 1:
                break
        b = pow(c, 1 << (m - i - 1), p)
        r = (r * b) % p
        c = pow(b, 2, p)
        t = (t * c) % p
        m = i
    return r

# Calcul de G.y
y_square = (pow(x_G, 3, p) + A * pow(x_G, 2, p) + x_G) % p
y_G = modular_sqrt(y_square, p)
G = (x_G, y_G)

print(f"[+] Générateur trouvé : G = ({G[0]}, {G[1]})")

# --- 2. ARITHMÉTIQUE DE MONTGOMERY (AFFINE) ---
def add_points(P, Q, A, B, p):
    if P is None: return Q
    if Q is None: return P
    x1, y1 = P
    x2, y2 = Q
    
    if x1 == x2:
        if y1 == y2:
            return double_point(P, A, B, p)
        else:
            return None  # Point à l'infini
            
    num = (y2 - y1) % p
    denom = (x2 - x1) % p
    alpha = (num * pow(denom, -1, p)) % p
    
    x3 = (B * pow(alpha, 2, p) - A - x1 - x2) % p
    y3 = (alpha * (x1 - x3) - y1) % p
    return (x3, y3)

def double_point(P, A, B, p):
    if P is None: return None
    x1, y1 = P
    if y1 == 0: return None
    
    num = (3 * pow(x1, 2, p) + 2 * A * x1 + 1) % p
    denom = (2 * B * y1) % p
    alpha = (num * pow(denom, -1, p)) % p
    
    x3 = (B * pow(alpha, 2, p) - A - 2 * x1) % p
    y3 = (alpha * (x1 - x3) - y1) % p
    return (x3, y3)

# --- 3. L'ÉCHELLE DE MONTGOMERY (MONTGOMERY'S LADDER) ---
def montgomery_ladder(P, k, A, B, p):
    bits = bin(k)[2:]  # Représentation binaire du scalaire
    
    # Étape 1 : Initialisation
    R0 = P
    R1 = double_point(P, A, B, p)
    
    # Étape 2 : Boucle du bit n-2 jusqu'à 0
    for bit in bits[1:]:
        if bit == '0':
            new_R1 = add_points(R0, R1, A, B, p)
            new_R0 = double_point(R0, A, B, p)
        else:
            new_R0 = add_points(R0, R1, A, B, p)
            new_R1 = double_point(R1, A, B, p)
        R0, R1 = new_R0, new_R1
        
    return R0

# --- 4. EXÉCUTION ---
Q = montgomery_ladder(G, k, A, B, p)
print(f"\n[★] Coordonnée X de Q (décimal) : {Q[0]}")