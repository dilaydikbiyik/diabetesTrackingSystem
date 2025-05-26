import hashlib

def hashle(sifre):
    return hashlib.sha256(sifre.encode()).digest()
