from passlib.context import CryptContext

ctx_pw = CryptContext(
    schemes   = ['argon2'],
    deprecated = 'auto'
)

pw = 'abcd1234'

def crypt(txt):
    return ctx_pw.hash(txt)

hashed = crypt(pw)
print(hashed)

def verify(orig, hashed):
    return ctx_pw.verify(orig, hashed)

print(1, verify(pw, hashed))
print(2, verify('abcd1235', hashed))