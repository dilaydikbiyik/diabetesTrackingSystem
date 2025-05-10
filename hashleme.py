import hashlib
from uu import encode


def hashle(sifre):
    return hashlib.sha256(sifre.encode()).digest()