from otp import *
from zlib import crc32



a = (Gen_blockids(0,0))
#Save_blockids(0,0,a)

cdr = Otp_coder(0)
cdr.loadpickle(0)

k = cdr.encryptblock(0,bytes("I wouldn't mind a can of Einstok",'utf-8'))
print(k)
print(len(k[0] + k[1] + k[2]))
#print(Gen_disposables(100))
