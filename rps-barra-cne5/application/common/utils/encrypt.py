# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
import base64

def encrypt(encrypt_str, security_key):
    """
    加密

    :param encrypt_str: 需加密字符串
    :param security_key: 密钥
    :return:
    """
    bs = AES.block_size
    pad = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)
    key = base64.b64decode(security_key)
    cryptor = AES.new(key, AES.MODE_ECB)
    s = cryptor.encrypt(pad(encrypt_str).encode("utf-8"))
    s = base64.b64encode(s)
    s = s.decode("utf-8")
    return s

def decrypt(encrypt_str, security_key):
    """
    解密
    :param encrypt_str: 加密字符串
    :param security_key: 密钥
    :return: 解密后字符
    """
    key = base64.b64decode(security_key)
    cryptor = AES.new(key, AES.MODE_ECB)
    s = base64.b64decode(encrypt_str)
    s = cryptor.decrypt(s)
    s = bytes.decode(s)
    s = s.strip().rstrip().replace("\b", "").replace("\n", "").replace("\r", "").replace("\t", "").replace("",
                                                                                                           "").replace(
        "\x07", "").replace('\x04', "").replace('', '')
    return s


if __name__ == "__main__":
    aim = 'credit'
    base_en = "S0FJWVVEU1NQTE04ODg4OA=="
    r = encrypt(aim, base_en)
    print(f'加密:{r}')
    s = decrypt(r, base_en)
    print(f'解密:{s}')
    print(f'原始字符:{aim}')
