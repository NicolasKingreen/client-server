from random import choices
from string import ascii_letters
from datetime import datetime


def generate_username(length=8):
    letters = list(ascii_letters)
    digits = list(map(str, list(range(10))))
    allowed_symbols = letters + digits
    username = ''.join(choices(allowed_symbols, k=length))
    return username

def format_addr(addr):
    return f"{addr[0]}:{addr[1]}"

def get_time():
    return datetime.now().strftime("%H:%M:%S")

