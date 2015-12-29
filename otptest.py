from otp import *
from zlib import crc32

cdr = Otp_coder(0)
cdr.loadpads(0)
cdr.loadstate(0)


a = (cdr.encrypt("Bequerel",0))
print(a)
b = (cdr.decrypt(a[1],a[0]))
print(cdr.stats())
print(b)

print(available_dirs())

print(Gen_disposable())
