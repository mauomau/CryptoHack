#!/usr/bin/env python3

# pyrefly: ignore [missing-import]
from Crypto.Util.number import *
from pwn import *
import sys
# import this
import base64

# caractere attendu
def find_key(flag):
    """
    Calcule et affiche la clé de XOR potentielle en comparant les premiers octets
    du message chiffré (fourni en hexadécimal) avec le préfixe attendu "crypto".

    Args:
        flag (str): Le message chiffré sous forme de chaîne hexadécimale.
        
    Exemple:
        >>> find_key("73626960647f...")
        Cle (raw)      : b'\\x10\\x10\\x10\\x10\\x10\\x10'
        Cle (entiers)  : [16, 16, 16, 16, 16, 16]
    """
    expected_flag = b"crypto{"
    flag_bytes = bytes.fromhex(flag)
    
    key_bytes = bytes(f ^ e for f, e in zip(flag_bytes[:len(expected_flag)], expected_flag))
    print("Cle (raw)      :", key_bytes)
    print("Cle (entiers)  :", list(key_bytes))
    


if sys.version_info.major == 2:
    print("You are running Python 2, which is no longer supported. Please update to Python 3.")

ords = [81, 64, 75, 66, 70, 93, 73, 72, 1, 92, 109, 2, 84, 109, 66, 75, 70, 90, 2, 92, 79]
ords2 = [99, 114, 121, 112, 116, 111, 123, 65, 83, 67, 73, 73, 95, 112, 114, 49, 110, 116, 52, 98, 108, 51, 125]
hex = "63727970746f7b596f755f77696c6c5f62655f776f726b696e675f776974685f6865785f737472696e67735f615f6c6f747d"
b64 = "72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf"
long_byte = 11515195063862318899931685488813747395775516287289682636499965282714637259206269
xor_item = "label"

# print("Here is your flag:")
#print("".join(chr(o) for o in ords2))
# print(bytes.fromhex(hex).decode())

# print(base64.b64encode(bytes.fromhex(b64))) 

# print(long_to_bytes(long_byte))

# print("".join( chr(ord(x) ^ 13) for x in xor_item ))


# hex_key1 = "a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313"
# hex_v3   = "c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1" 
# hex_v4   = "04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf"

# b_key1 = bytes.fromhex(hex_key1)
# b_v3   = bytes.fromhex(hex_v3)
# b_v4   = bytes.fromhex(hex_v4)

# flag_bytes = bytes(v4_byte ^ v3_byte ^ key1_byte for v4_byte, v3_byte, key1_byte in zip(b_v4, b_v3, b_key1))
# print(flag_bytes.decode())

final = "73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d"
# fin_byte = bytes.fromhex(final)

# print(""
# .join( chr(b ^ 16) for b in fin_byte))

flag = "0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104"
flag_bytes = bytes.fromhex(flag)
key = b'myXORkey'
key_len = len(key)

# flag_bytes = bytes(flag_bytes[i] ^ key[i % key_len ] for i in range(len(flag_bytes)) )

# print(flag_bytes.decode())


key = xor(flag_bytes[:7], 'crypto{') + xor(flag_bytes[-1], '}')
print(key)

# find_key(flag)
print(xor(flag_bytes, b"myXORkey"))