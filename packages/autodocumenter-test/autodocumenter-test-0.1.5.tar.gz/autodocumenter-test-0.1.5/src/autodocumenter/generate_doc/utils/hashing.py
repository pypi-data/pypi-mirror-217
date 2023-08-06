import hashlib


def get_hash(*args):
    hasher = hashlib.sha256(usedforsecurity=True)
    for arg in args:
        if not isinstance(arg, str):
            arg = str(arg)
        arg = bytes(arg, "utf-8")
        hasher.update(arg)
    hash = hasher.hexdigest()
    return hash
