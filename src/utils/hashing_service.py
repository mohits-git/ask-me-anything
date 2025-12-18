import bcrypt

_cost = 12


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=_cost)
    hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash.decode('utf-8')


def verify_hashed_password(password: str, hash: str):
    return bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'))
