import os
import random
import string

def generate_random_filename(filename):
    random_string = ''.join(random.choices(
        string.ascii_letters + string.digits, k=16))
    name, ext = os.path.splitext(filename)
    random_filename = f'{random_string}-{name}{ext}'
    return random_filename