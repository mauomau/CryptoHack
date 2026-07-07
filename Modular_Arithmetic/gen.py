import os

# Contenu intégral et ultra-détaillé structuré pour Obsidian
markdown_content = """---
tags:
  - cryptography
  - cryptohack
  - math
  - ctf-cheat-sheet
---

# 🧠 CryptoHack : Arithmétique Modulaire (Fiche Complète de Révision CTF)

> [!info] Note de référence
> Ce fichier consolide les concepts fondamentaux de "Intro to crypto hack.md"[cite: 1] et y ajoute les techniques avancées d'attaque indispensables pour les compétitions de CTF.

---

## 1. Encodage et Représentation des Données

Les systèmes cryptographiques comme RSA manipulent exclusivement des structures numériques[cite: 1]. Les messages textuels doivent donc être convertis mathématiquement[cite: 1].

### ASCII (American Standard Code for Information Interchange)
* ASCII est un standard d'encodage sur 7 bits permettant de représenter du texte à l'aide des entiers allant de 0 à 127[cite: 1].
* **Fonctions Python clés**[cite: 1] :
  * `chr(x)` : Convertit un entier ordinal ASCII en son caractère correspondant[cite: 1].
  * `ord(c)` : Fait l'inverse (caractère vers entier ordonné)[cite: 1].
* **Exemple de tableau d'entiers à décoder**[cite: 1] :
  `[99, 114, 121, 112, 116, 111, 123, 65, 83, 67, 73, 73, 95, 112, 114, 49, 110, 116, 52, 98, 108, 51, 125]`[cite: 1]

### Conversion de Messages en Grands Entiers (Pipeline Hexadécimal)
La méthode standard consiste à extraire les octets ordinaux du message, les convertir en hexadécimal, puis les concaténer[cite: 1]. Ce résultat peut être lu comme un nombre en base 16 ou en base 10[cite: 1].

**Illustration concrète du pipeline**[cite: 1] :
* Message : `HELLO`[cite: 1]
* Octets ASCII : `[72, 69, 76, 76, 79]`[cite: 1]
* Octets Hexadécimaux : `[0x48, 0x45, 0x4c, 0x4c, 0x4f]`[cite: 1]
* Base 16 (Hex) : `0x48454c4c4f`[cite: 1]
* Base 10 (Décimal) : `310400273487`[cite: 1]

**Implémentation Python (Bibliothèque PyCryptodome)**[cite: 1] :
```python
from Crypto.Util.number import bytes_to_long, long_to_bytes

# Conversion d'une chaîne d'octets en un entier géant
integer_value = bytes_to_long(b"HELLO")

# Reconversion de l'entier géant vers le message original
original_message = long_to_bytes(integer_value)

```

---

## 2. L'Algorithme d'Euclide Étendu (Extended GCD)

Étant donné deux entiers positifs $a$ et $b$, l'algorithme d'Euclide étendu permet de calculer efficacement deux entiers coefficients $u$ et $v$ tels que :


$$a \cdot u + b \cdot v = \gcd(a, b)$$

> [!important] Règle d'or CTF
> Cet algorithme est indispensable pour calculer **l'inverse modulaire** (par exemple, pour retrouver l'exposant privé $d$ à partir de l'exposant public $e$ lors du déchiffrement RSA).
> Si $p$ et $q$ sont deux nombres premiers distincts, leur plus grand commun diviseur $\gcd(p, q)$ sera toujours égal à $1$.
> 
> 

---

## 3. Fondations de l'Arithmétique Modulaire

L'arithmétique modulaire est l'étude des restes de divisions entières (souvent comparée à la lecture de l'heure sur une horloge de 12 heures).

### Congruences et Propriétés

* Deux entiers $a$ et $b$ sont dits congrus modulo $m$ (noté $a \equiv b \pmod m$) si la division de $a$ par $m$ donne pour reste $b$.


* Cela signifie également que $m$ divise parfaitement la différence $a - b$. Si $m$ divise $a$, alors $a \equiv 0 \pmod m$.



### Corps Finis $\mathbb{F}_p$ vs Anneaux $\mathbb{Z}_n$

* Si le modulo choisi est un nombre premier $p$, l'ensemble des entiers $\{0, 1, \dots, p-1\}$ définit un **Corps Fini** noté $\mathbb{F}_p$. Dans un corps fini, chaque élément non nul possède obligatoirement un inverse additif et un inverse multiplicatif unique.


* Si le modulo est un nombre composé $n$ (non premier), l'ensemble définit un **Anneau**.



### Petit Théorème de Fermat

Pour tout nombre premier $p$ et tout entier $a$ non multiple de $p$, on a la garantie mathématique que :


$$a^{p-1} \equiv 1 \pmod p$$

> [!tip] Astuce de calcul
> Grâce à ce théorème, calculer des puissances géantes modulo $p$ devient trivial si l'exposant est un multiple de $p-1$. En Python, l'inverse modulaire se calcule instantanément via `pow(a, -1, p)`.
> 
> 

---

## 4. Le Théorème des Restes Chinois (CRT)

Le Théorème des Restes Chinois (CRT) fournit une solution unique à un système de plusieurs congruences linéaires, à condition que tous les modulos soient **copremiers entre eux deux à deux** ($\gcd(n_i, n_j) = 1$).

### Cas d'usage en CTF

En cryptographie, le CRT est massivement utilisé pour décomposer un calcul sur un entier gigantesque en plusieurs sous-calculs indépendants sur des modules beaucoup plus petits et simples à traiter.

### Formule de reconstruction (Exemple CryptoHack) :

Pour le système d'équations suivant :


$$x \equiv 2 \pmod 5$$

$$x \equiv 3 \pmod{11}$$

$$x \equiv 5 \pmod{17}$$

L'unique solution $x \equiv a \pmod N$ (où $N = 5 \cdot 11 \cdot 17 = 935$) se calcule automatiquement via ce script :

```python
a = [2, 3, 5]
n = [5, 11, 17]

N = 1
for mod in n:
    N *= mod

x = 0
for a_i, n_i in zip(a, n):
    N_i = N // n_i
    M_i = pow(N_i, -1, n_i)  # Calcul de l'inverse modulaire
    x += a_i * N_i * M_i

flag = x % N
print(f"La solution unique (le flag) est : {flag}")

```

---

## 5. Résidus Quadratiques & Symbole de Legendre

Un entier $a$ est un **résidu quadratique** (un carré parfait modulaire) s'il existe un nombre $x$ tel que :


$$x^2 \equiv a \pmod p$$

### Le Détecteur Mathématique (Critère d'Euler)

Pour déterminer si un nombre géant $a$ est un carré parfait, on utilise le Symbole de Legendre en calculant : `pow(a, (p - 1) // 2, p)`.

* Si le résultat est **`1`** : $a$ est un carré parfait.
* Si le résultat est **`p - 1` (ou `-1`)** : $a$ n'est pas un carré parfait.

### Le secret des "Équipes" Modulo 4

Tous les nombres premiers du monde appartiennent à l'une de ces deux catégories :

1. **L'équipe $p \equiv 1 \pmod 4$**
2. **L'équipe $p \equiv 3 \pmod 4$**

> [!abstract] Astuce de calcul mental CTF
> Pour connaître l'équipe de $p$, prends uniquement ses **deux derniers chiffres** et fais `% 4` (car 100 est un multiple parfait de 4).
> *Exemple :* Si $p$ se termine par `51`, on calcule $51 \pmod 4 = 3$. Le nombre fait partie de l'équipe $3 \pmod 4$.

### Règle d'or de l'équipe $3 \pmod 4$ (Attaque du défi *Adrien's Signs*)

Dans le monde mathématique des modulos de l'équipe $3 \pmod 4$, **le nombre $-1$ n'est jamais un carré parfait**.

* Si une base $a$ est un carré parfait, alors $a^e$ sera **toujours** un carré parfait (le symbole de Legendre renverra `1`), peu importe la valeur de l'exposant secret $e$.
* Si on applique un signe moins à ce nombre, $-a^e \pmod p$, il se transforme **obligatoirement en un non-carré** (le symbole de Legendre renverra `p - 1`).

**Logique de décodage :**

* `Symbole de Legendre == 1` $\implies$ Pas de signe moins $\implies$ Le bit original vaut `1`.
* `Symbole de Legendre == p - 1` $\implies$ Présence d'un signe moins $\implies$ Le bit original vaut `0`.

### Calcul des racines carrées

* **Si $p \equiv 3 \pmod 4$** : La formule de Fermat donne la racine instantanément : `pow(a, (p + 1) // 4, p)`.
* **Si $p \equiv 1 \pmod 4$** : La formule directe échoue, il faut obligatoirement implémenter l'algorithme de **Tonelli-Shanks**.
* *Rappel* : Un carré modulaire possède deux racines : `r` et `p - r`. L'énoncé précisera s'il faut renvoyer la plus petite (`min`) ou la plus grande (`max`).

---

## 6. L'Attaque de la "Gomme Magique" (Modular Binomials)

> [!abstract] Règle de réduction de Modulo
> Si une équation mathématique est valide modulo $N$ (où $N = p \cdot q$), elle est **automatiquement valide** modulo ses diviseurs individuels $p$ et $q$.

### Principe de la gomme modulaire

Le modulo n'est rien d'autre que le reste d'une division entière (le nombre de jetons restants après avoir constitué des paquets complets).
Travailler modulo $p$ agit comme une gomme magique : **tout terme multiplié par $p$ tombe pile dans un paquet parfait, son reste devient égal à $0$ et il disparaît complètement du calcul**.


$$4 \cdot p \equiv 0 \pmod p$$

### Résolution pas à pas de l'attaque

Face à un système complexe de binômes modulaires du type :


$$c_1 = (2p + 3q)^{e_1} \pmod N$$

$$c_2 = (5p + 7q)^{e_2} \pmod N$$

1. **On applique la gomme modulo $p$** : Les blocs contenant $p$ s'annulent ($2p \equiv 0$ et $5p \equiv 0$).

$$c_1 \equiv (3q)^{e_1} \equiv 3^{e_1} \cdot q^{e_1} \pmod p$$


$$c_2 \equiv (7q)^{e_2} \equiv 7^{e_2} \cdot q^{e_2} \pmod p$$


2. **On égalise les puissances de l'inconnue $q$** : On réalise un produit croisé des exposants en élevant $c_1$ à la puissance $e_2$ et $c_2$ à la puissance $e_1$.

$$c_1^{e_2} \equiv 3^{e_1 e_2} \cdot q^{e_1 e_2} \pmod p$$


$$c_2^{e_1} \equiv 7^{e_1 e_2} \cdot q^{e_1 e_2} \pmod p$$


3. **On élimine $q$ par substitution** : On croise les constantes multiplicatives de devant pour rendre les membres de droite rigoureusement identiques, ce qui permet de l'isoler :

$$(7^{e_1 e_2} \cdot c_1^{e_2} - 3^{e_1 e_2} \cdot c_2^{e_1}) \equiv 0 \pmod p$$


4. **Extraction par PGCD (GCD)** : Cette grande soustraction donne un résultat qui est un multiple parfait de $p$. Comme $N$ est aussi un multiple de $p$, le calcul du Plus Grand Commun Diviseur entre cette formule et $N$ extrait directement le nombre premier secret $p$ :

$$p = \gcd\left((7^{e_1 e_2} \cdot c_1^{e_2} - 3^{e_1 e_2} \cdot c_2^{e_1}) \pmod N, N\right)$$



"""

# Écriture du fichier sur le disque

filename = "Notes_CryptoHack_Complet.md"
try:
    with open(filename, "w", encoding="utf-8") as f:
        f.write(markdown_content)
        print(f"[+] Succès ! Le fichier '{filename}' a été généré.")
        print(
            "[+] Tu peux maintenant le glisser-déposer directement dans ton coffre Obsidian."
        )
except Exception as e:
    print(f"[-] Une erreur est survenue lors de la création du fichier : {e}")
