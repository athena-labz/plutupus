import base64

def token_to_hex(token):
    return bytes.decode(base64.b16encode(bytes(token, "utf-8")), "utf-8")