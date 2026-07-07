import hashlib
import urllib.request
from Crypto.Cipher import AES

# Ciphertext retrieved from http://aes.cryptohack.org/passwords_as_keys/encrypt_flag/
ciphertext_hex = "c92b7734070205bdf6c0087a751466ec13ae15e6f1bcdd3f3a535ec0f4bbae66"
ciphertext = bytes.fromhex(ciphertext_hex)

# Try opening the local words file, fallback to downloading if not found
try:
    with open("/usr/share/dict/words") as f:
        words = [w.strip() for w in f.readlines()]
except FileNotFoundError:
    url = "https://gist.githubusercontent.com/wchargin/8927565/raw/d9783627c731268fb2935a731a618aa8e95cf465/words"
    print("Local /usr/share/dict/words not found. Downloading dictionary...")
    with urllib.request.urlopen(url) as response:
        words = response.read().decode('utf-8').splitlines()

print(f"Loaded {len(words)} words. Starting brute-force...")

for word in words:
    # Key is the MD5 hash of the word
    key = hashlib.md5(word.encode()).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    try:
        decrypted = cipher.decrypt(ciphertext)
        if b"crypto{" in decrypted:
            print(f"[+] Password found: {word}")
            print(f"[+] Flag: {decrypted.decode()}")
            break
    except Exception:
        continue
