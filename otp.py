def encrypt(ba_str,ba_pad):
    el = bytearray()
    for a in range(0,len(ba_str)):
        el.append(ba_str[a] ^ ba_pad[a])

    return el
def decrypt(string,pad):
    pass

a = bytearray("Test1234",'UTF-8')
b = bytearray("1234Test",'UTF-8')


print(encrypt(encrypt(a,b),b))
