import hashlib

# md5加密
def my_md5(value):
    m=hashlib.md5()
    m.update(value.encode('utf-8'))
    return m.hexdigest()
