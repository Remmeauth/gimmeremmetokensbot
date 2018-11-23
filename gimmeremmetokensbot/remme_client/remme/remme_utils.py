import hashlib
import base64
import math
import random
import re
from remme_client.remme.constants.remme_patterns import RemmePatterns


def is_valid_batch_id(_batch_id):
    return re.match(RemmePatterns.HEADER_SIGNATURE.value, _batch_id) is not None


def bytes_to_hex(_bytes):
    # print(f"functions; bytes_to_hex args: {_bytes}")
    result = utf8_to_bytes(_bytes).hex()
    # print(f"functions; bytes_to_hex result: {result}")
    return result


def base64_to_dict(_base64):
    return eval(base64.b64decode(_base64))


def dict_to_base64(_dict):
    return base64.b64encode(str(_dict).encode('utf-8'))


def utf8_to_bytes(_string):
    return _string.encode('UTF-8')


def bytes_to_utf8(_bytes):
    return _bytes.decode('UTF-8')


def is_string_or_bytes(message):
    return isinstance(message, str) or isinstance(message, bytes)


def is_valid_hex_string(message):
    return isinstance(message, str) and is_hex(message)


def hex_to_bytes(message):
    if isinstance(message, bytes):
        return message
    if is_valid_hex_string(message):
        return bytes.fromhex(message)
    raise Exception("Invalid type of message given. Expected hex string or bytes.")


def generate_address(_family_name, _public_key_to):
    return "" + sha512_hexdigest(_family_name)[:6] + sha512_hexdigest(_public_key_to)[:64]


def generate_settings_address(key):
    key_parts = key.split(".")[:4]
    address_parts = [sha256_hexdigest(x)[0:16] for x in key_parts]
    while (4 - len(address_parts)) != 0:
        address_parts.append(sha256_hexdigest("")[0:16])
    return "000000" + "".join(address_parts)


def create_nonce():
    # print(f"utils; generate nonce")
    hash_o = hashlib.sha512(str(math.floor(1000 * random.random())).encode('UTF-8'))
    result = hash_o.hexdigest()
    # print(f"utils; generate nonce result: {result}")
    return result


def sha512_hexdigest(data):
    return hashlib.sha512(data.encode('utf-8') if isinstance(data, str) else data).hexdigest()


def sha256_hexdigest(data):
    return hashlib.sha256(data.encode('utf-8') if isinstance(data, str) else data).hexdigest()


def is_hex(data):
    try:
        int(data, 16)
        return True
    except ValueError:
        return False
