p = 857504083339712752489993810777
q = 1029224947942998075080348647219
e = 65537

# 1. Calcul de l'indicatrice d'Euler
phi = (p - 1) * (q - 1)

# 2. Calcul de la clé privée d (inverse modulaire de e)
d = pow(e, -1, phi)

# print(d)

# Les nombres premiers des leçons précédentes
p = 857504083339712752489993810777
q = 1029224947942998075080348647219

# Paramètres fournis dans ce défi
N = 882564595536224140639625987659416029426239230804614613279163
e = 65537
c = 77578995801157823671636298847186723593814843845525223303932

# 1. On recalcule phi(N) et la clé privée d
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)

# 2. On applique la formule de déchiffrement RSA : m = c^d mod N
message = pow(c, d, N)

print(f"Le message secret déchiffré est : {message}")