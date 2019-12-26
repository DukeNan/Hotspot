import hashlib


def get_md5(string: str):
    """
    获取MD5加密字符串
    """
    md5 = hashlib.md5()
    md5.update(string.encode(encoding='utf-8'))
    return md5.hexdigest()


if __name__ == '__main__':
    a = get_md5('123456')
    print(a)
