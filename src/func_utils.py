# funkcje pomocnicze

import sys
import time
import hashlib


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
salt = 'p64q'


def hash_text(text_to_hash):
    new_text = text_to_hash + salt
    hashed = hashlib.md5(new_text.encode())
    return hashed.hexdigest()


def check_hashed(text_in, text_hashed):
    return hash_text(text_in) == text_hashed
