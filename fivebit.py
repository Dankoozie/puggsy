dic1024 = {}
#5bit encoding / compression

#26 - Spás
#27 - Change to UCase
#28 - Numeric/Punc.
#29 - End/Dict32768
#30 - Dict1024
#31 - UTF-8 escape

def load_dict():
    f = open('mydict.csv','r')
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

    def desub(self,charlist,usedict = False):
        mos = {0:self.__desub_lcase,1:self.__desub_ucase,2:self.__desub_num,4:self.__desub_dic1024}
        string = ""
        mode = 0

        for a in charlist:
            (mode,st) = mos[mode](a)
            string += st

        return string

    def sub(self,str,usedict = False):
        cw = ""
        cl = []
        for a in str:
            cw += a
            if(ord(a) in range(97,123)): cl.append(ord(a) - 97)
            elif(ord(a) in range(65,91)):
                 cl.append(27)
                 cl.append(ord(a) - 65)
            elif(ord(a) == 32):
                cl.append(26)
                wordcode = search_dict(cw.rstrip())
             
                if(wordcode != -1):
                     cl = cl[:len(cl) - len(cw)]
                     cl.append(30)
                     cl.append(wordcode >> 5)
                     cl.append(wordcode & 31)
                cw = ""
            elif(ord(a) in range(33,64)):
                cl.append(28)
                cl.append(ord(a) - 33)
            else:
                #UTF-8
                continue

        return cl

def encode3(charlist):
    nexstep = {0:(5,3), 1:(6,2), 2:(7,1), 3:(0,0), 4:(1,-1,1,7), 5:(2,-2,3,6), 6:(3,-3,7,5), 7:(4,-4,15,4) }
    curbyte = 0
    bstr = []
    step = 0

    for a in charlist:
        curbyte = curbyte | shift(a,nexstep[step][1]) 
        if(step > 2):
            bstr.append(curbyte)
            curbyte = 0
            if(step > 3):
                curbyte = (a & nexstep[step][2]) << nexstep[step][3]
        step = nexstep[step][0]

    if step in range(1,5):
        bstr.append(curbyte)
    
    return bytes(bstr)

def drawchars(byte,nbits,nbitsl):
    tot = 8 + nbitsl
    itot = (nbits << 8) | byte
    if(tot < 10):
        c1 = itot >> (tot - 5) & 31
        newnbits = itot & (2**(tot -5) -1)
        newnbitsl = tot - 5
        return(([c1],newnbits,newnbitsl,False))
    elif(tot > 9):
         c1 = itot >> (tot - 5) & 31
         c2 = itot >> (tot - 10) & 31
         newnbits = itot & (2**(tot - 10)-1)
         newnbitsl = tot - 10
         return(([c1,c2],newnbits,newnbitsl,False))
    
def decode3(string):
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

    print ("Bits left: ", nbl)
    return ls
                                

          


load_dict()

s = Substitute()








