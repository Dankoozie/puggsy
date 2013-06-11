dic1024 = {}
#5bit encoding / compression
#0-25 - abcdefghijklmnopqrstuvwxyz
#26 - Spás
#27 - Change to UCase
#28 - Numeric/Punc.  
#29 - End/Dict32768
#30 - Dict1024
#31 - UTF-8 escape

from math import ceil

def load_dict():
    f = open('d1024_1.csv','r')
    for i in range(0,1024):
        cw = f.readline()
        if(len(cw.rstrip()) > 2): dic1024[i] = cw.rstrip()
        
def search_dict(word):
    for k in dic1024:
        if(word == dic1024[k]): return k
    return -1

def shift(val,amt):
    if(amt > 0):
        return(val << amt)
    if(amt < 0):
        return(val >> abs(amt))
    return val

class Substitute:
    def __init__(self):
        self.dict_last = False
        self.dict_fchar = 0
        self.unicode_len = 0
        self.unicode_buffer = []

    #Desub functions
    def __desub_lcase(self,a):
        if(a > 26):
            return((a - 26,""))
        else:
            if(a != 26):
                return((0,chr(a+97)))
            else:
                return((0," "))
                   
    def __desub_ucase(self,a):
        return((0,chr(a + 65)))
        
    def __desub_num(self,a):
        return((0,chr(a + 33)))

    def __desub_dic1024(self,a):
        if(not self.dict_last):
            self.dict_fchar = a
            self.dict_last = True
            return((4,""))
        else:
            self.dict_last = False
            return(0,dic1024[((self.dict_fchar << 5) | a)] + " ")
        
    def __desub_unicode(self,a):
        if(self.unicode_len == 0):
            self.unicode_len = a
            return((5,""))
        elif(self.unicode_len > 0):
            self.unicode_buffer.append(a)
            
            if(self.unicode_len == len(self.unicode_buffer)):
                char = self.__get_unicode(self.unicode_buffer)
                self.unicode_len = 0
                self.unicode_buffer = []
                return((0,char))
            return((5,""))
        
    #Unicode gen/get
    def __gen_unicode(self,char):
        ordn = ord(char)
        bl = ordn.bit_length()
        li = [31,ceil((bl) / 5)]

        for i in range(0,li[1]):
            li.append(((ordn >> 5*i) & 31))

        return li

    def __get_unicode(self,clist):
        ccode = 0
        for i in range(0,len(clist)):
            ccode = (ccode << 5) + (clist[len(clist) - i - 1] & 31)
            print (ccode)
        return chr(ccode)

    def desub(self,charlist,usedict = False):
        self.unicode_len = 0 # Reset unicode len
        self.unicode_buffer = [] # and buffer
        
        mos = {0:self.__desub_lcase,1:self.__desub_ucase,2:self.__desub_num,4:self.__desub_dic1024,5:self.__desub_unicode}
        string = ""
        mode = 0

        for a in charlist:
            (mode,st) = mos[mode](a)
            string += st

        return string

    def sub(self,str_in,usedict = False):
        #not supported = 0-32, 92-96)
        cw = ""
        cl = []
        for a in str_in:
            cw += a
            if(ord(a) in range(97,123)): cl.append(ord(a) - 97)
            elif(ord(a) in range(65,91)): cl.extend([27,ord(a) - 65])
            elif(ord(a) == 32):
                cl.append(26)
                wordcode = search_dict(cw.rstrip())             
                if(wordcode != -1):
                     cl = cl[:len(cl) - len(cw)]
                     cl.extend([30,wordcode >> 5,wordcode & 31])
                cw = ""
            elif(ord(a) in range(33,64)): cl.extend([28,ord(a) - 33])
            else:
                #UTF-8
                cl.extend(self.__gen_unicode(a))


        #Throw in blank character if more than 5 bits free
        BitsFree = 8 - (len(cl) * 5) % 8
        if( (BitsFree > 4) and (BitsFree != 8) ):
            cl.append(29)
            

        return cl

def encode(charlist):
    #Converts a list of 5-bit values (0-31) into byte string
    nexstep = {0:(5,3), 1:(6,2), 2:(7,1), 3:(0,0), 4:(1,-1,1,7), 5:(2,-2,3,6), 6:(3,-3,7,5), 7:(4,-4,15,4) }
    curbyte = 0
    bstr = []
    step = 0

    ByteLeft = False

    for a in charlist:
        curbyte = curbyte | shift(a,nexstep[step][1])
        ByteLeft = True
        if(step > 2):
            bstr.append(curbyte)
            curbyte = 0
            ByteLeft = False
            if(step > 3):
                curbyte = (a & nexstep[step][2]) << nexstep[step][3]
                ByteLeft = True
        step = nexstep[step][0]
        
    if ByteLeft:
        bstr.append(curbyte)
    
    return bytes(bstr)

def drawchars(byte,nbits,nbitsl):
    tot = 8 + nbitsl
    itot = (nbits << 8) | byte
    if(tot < 10):
        c1 = itot >> (tot - 5) & 31
        newnbits = itot & (2**(tot -5) -1)
        newnbitsl = tot - 5
        return(([c1],newnbits,newnbitsl))
    elif(tot > 9):
         c1 = itot >> (tot - 5) & 31
         c2 = itot >> (tot - 10) & 31
         newnbits = itot & (2**(tot - 10)-1)
         newnbitsl = tot - 10
         return(([c1,c2],newnbits,newnbitsl))
    
def decode(string):
    bs = bytes(string)
    nbl = 0
    nbs = 0
    ls = []
    ns = None
    for a in bs:
        rs = drawchars(a,nbs,nbl)
        nbs = rs[1]
        nbl = rs[2]
        ls.extend(rs[0])
    return ls

load_dict()
s = Substitute()


def compress(string):
    return(encode(s.sub(string)))

def decompress(string):
   return(s.desub(decode(string)))
