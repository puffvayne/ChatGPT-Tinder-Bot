import hashlib


def get_md5(s: str) -> str:
    # Create a new md5 hash object
    hash_object = hashlib.md5()

    # Encode the input string to bytes, since the md5 function requires bytes
    input_bytes = s.encode('utf-8')

    # Update the hash object with the bytes of the string
    hash_object.update(input_bytes)

    # Get the hexadecimal representation of the hash
    md5_hash = hash_object.hexdigest()

    return md5_hash
