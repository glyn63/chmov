import random

allowed_chars = '23456789abcdefghijkmnpqrstuvwxyz'
random_code = ''.join(random.choices(allowed_chars, k=6))

print(random_code)

