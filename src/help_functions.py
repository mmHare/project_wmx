# funkcje pomocnicze

from cryptography.fernet import Fernet
import sys
import time
import hashlib
import types
import os
from src.globals import *


def clear_screen():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For macOS and Linux
    else:
        os.system('clear')

# animacje oczekiwania


def waiting_animation_dot(repeat=3, dot_count=3, delay=0.5):
    for _ in range(repeat):
        for i in range(1, dot_count + 1):
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(delay)
        sys.stdout.write('\r   \r')


def waiting_animation_spinner(duration=5, delay=0.1):
    spinner = ['|', '/', '-', '\\']
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write('\r' + spinner[i % len(spinner)])
        sys.stdout.flush()
        time.sleep(delay)
        i += 1
    sys.stdout.write('\r \r')


# enkrypcja i haszowanie


# def hash_text(text_to_hash):
#     new_text = text_to_hash + salt
#     hashed = hashlib.md5(new_text.encode())
#     return hashed.hexdigest()


def hash_text(text_to_hash: str) -> str:
    new_text = text_to_hash + HASH_SALT
    return hashlib.sha256(new_text.encode()).hexdigest()


def check_hashed(text_in, text_hashed):
    return hash_text(text_in) == text_hashed

###################


# # Example
# hashed_value = hash_string("my_secret_password")
# print(hashed_value)
# Fernet key generated once via Fernet.generate_key()


def encrypt_data(secret_data):
    try:
        fernet = Fernet(ENCRYPT_KEY)
        return fernet.encrypt(secret_data.encode())
    except Exception as e:
        print(f"Encryption error: {e}")


def decrypt_data(token):
    try:
        fernet = Fernet(ENCRYPT_KEY)
        return fernet.decrypt(token).decode()
    except Exception as e:
        if token == "":
            return ""
        else:
            print(f"Decryption error: {e}")

# token = fernet1.  # encode() → bytes
# print("Encrypted:", token)

# # Step 3: Decrypt using key1
# retrieved_data = fernet1.decrypt(token).decode()  # decode() → str
# print("Decrypted:", retrieved_data)

    # # print("Encrypted:", token)

    # print("Decrypted:", fernet.decrypt(token).decode())
