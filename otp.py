#Python one-time pad encryption module
from zlib import crc32
from struct import unpack,pack

file_num = 0
offset = 0

class Otp_coder:

    def savestate(self,cid):
        sf = open("./otp/" + str(cid) + "/state.txt","w")
        sf.write("0\n") # Default file pair in use
        sf.write("0:" + str(self.in_offset) + ":" + str(self.out_offset) + "\n")
        sf.close()

    def loadstate(self,cid):
        sf = open("./otp/" + str(cid) + "/state.txt","r")
        self.in_file_active = self.out_file_active = int(sf.readline())
        (fid,io,oo) = sf.readline().split(":")
        self.in_file_active = int(fid)
        self.out_file_active = int(fid)
        self.in_offset = int(io)
        self.out_offset = int(oo)

    def loadpads(self,cid):
        f = open("./otp/" + cid + "/in.0","rb")
        o = open("./otp/" + cid + "/in.0","rb")
        self.in_contents = f.read()
        self.out_contents = o.read()
        f.close()
        o.close()
    
    def __init__(self,contact_id):
        functional = False
        self.in_file_list = {}
        self.in_file_active = 0 
        self.in_contents = b""
        self.in_offset = 0
        self.out_file_list = {}
        self.out_file_active = 0
        self.out_contents = b""
        self.out_offset = 0
        self.loadpads("0")

    

    def encrypt(self,ba_str,file = 0):
        send_offset = self.out_offset  #Offset value for sending to other party (initial offset of message)    
        cs = 0
        el = bytearray()
        for a in range(0,len(ba_str)):
            el.append(ba_str[a] ^ self.out_contents[a+self.out_offset])

        self.out_offset = self.out_offset + len(ba_str)

        
        xorlong = unpack(">L",self.out_contents[self.out_offset:self.out_offset+4])
        cs = (crc32(ba_str) ^ xorlong[0])        
        self.out_offset = self.out_offset + 4
        self.savestate(0)
        return (pack(">BQL",0,send_offset,cs),el)

    def decrypt(self,ba_str,bql):
        (file,offset,crc) = unpack(">BQL",bql)

        if(offset < self.in_offset):
            print("Offset less than internal state / Possible pad reuse")

        
        d_str = bytearray()
        for a in ba_str:
            d_str.append(a ^ self.in_contents[offset])
            offset = offset + 1


        xorlong = unpack(">L",self.in_contents[offset:offset+4])
        
        if(crc32(d_str) == crc ^ xorlong[0]):
            self.in_offset = offset + 4
            self.savestate(0)
            return (True,d_str)
        else:
            return(False,"")

