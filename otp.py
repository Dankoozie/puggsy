#Python one-time pad encryption module
from zlib import crc32
from struct import unpack,pack



file_num = 0
offset = 0



class Otp_manager:

    def loadpad(self,file):
        f = open("pad.bin","rb")
        self.pf = f.read(4096)
        f.close()

    
    def __init__(self,contact_id):
        functional = False
        in_file_list = {}
        in_file_active = 0
        in_offset = 0
        out_file_list = {}
        out_file_active = 0
        out_offset = 0
        self.loadpad("pf.bin")

    

    def encrypt(ba_str,usechecksum = True):
        cs = 0
        el = bytearray()
        for a in range(0,len(ba_str)):
            el.append(ba_str[a] ^ self.pf[a+offset])

        self.out_offset = self.out_offset + len(ba_str)

        
        xorlong = unpack(">L",pf[self.out_offset:self.out_offset+4])
        cs = (crc32(ba_str) ^ xorlong[0])        
        self.out_offset = self.out_offset + 4

        return (pack(">BQL",0,self.out_offset,cs),el)

    def decrypt(ba_str,usechecksum = True,crc = 0):
        pass

   # def encrypt(self,ba_str,usechecksum = True):
    #    pass





def decrypt(ba_str,checksum):
    pass

a = bytearray("Test1234",'UTF-8')
b = bytearray("1234Test",'UTF-8')



s = Otp_manager(255)
#
