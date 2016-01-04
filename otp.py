#Python one-time pad encryption module
from zlib import crc32
from struct import unpack,pack
from math import floor
import pickle
from os import listdir
from os.path import getsize
import entropy
import hmac

RNDSource = '/dev/urandom'
OTPDir = "./otp/"
BLOK_SIZE=512
disposables_target = 64
HASHFUNC = 'sha256'


file_num = 0
offset = 0

class Otp_creator:

    def __init__():
        pass

def available_dirs():
    ld = listdir(OTPDir)
    return ld

def Gen_disposable():
    rs = open(RNDSource,'rb')
    bn = rs.read(8)
    return(unpack(">Q",bn)[0])

def Gen_disposables(qty):
    lst = []
    for i in range(1,qty):
        lst.append(Gen_disposable())
    return lst

def Gen_blockids(padid,fileid):
    rs = open(RNDSource,'rb')
    bn = floor(getsize(OTPDir +  str(padid) + "/" + "in." + str(fileid))/BLOK_SIZE)
    bids = {}
    print("File is " + str(bn) + " blocks long")
    for a in range(bn):
        newrand = 0
        while(True):
            #Loop to prevent clashes
            newrand = unpack(">Q",rs.read(8))[0]
            newkey = rs.read(32)
            if(not newrand in bids.keys()):
                bids[newrand] = (a,newkey)
                break

        if(a/100 == int(a/100)): print( str(a) + " IDs generated")

    return bids

def Save_blockids(padid,fileid,bids):
    receptacle = open(OTPDir +  str(padid) + "/" + "blocks." + str(fileid),'wb')
    pickle.dump(bids,receptacle)
    receptacle.close()


class Otp_coder:

    def loadpickle(self,fid):
        #Outgoing pad
        lto = open(OTPDir +  str(self.contactid) + "/" + "blocks-out." + str(fid),'rb')
        self.blocks_out = pickle.load(lto)
        lto.close()

        #Incoming pad
        lfrom = open(OTPDir +  str(self.contactid) + "/" + "blocks-in." + str(fid),'rb')
        self.blocks_in = pickle.load(lfrom)
        lfrom.close()

    def savepickle(self,cid):
        sf = open(OTPDir + str(cid) + "/state.txt","w")

    def stats(self):
        pused_in = (self.in_offset / len(self.in_contents))*100
        pused_out = (self.out_offset / len(self.out_contents))*100

        return((round(pused_in,2),round(pused_out,2),self.in_offset,self.out_offset,len(self.in_contents),len(self.out_contents)))
    
    def __init__(self,contact_id):
        functional = False
        self.contactid = contact_id

    def getblok(self,padid,blokid,direction = 0):
        if(direction == 0): pdir = "/out."
        else: pdir = "/in."

        
        o = open(OTPDir + str(self.contactid) + pdir + str(padid),"rb")
        o.seek(blokid*BLOK_SIZE)
        return(o.read(BLOK_SIZE))

    def encryptblock(self,padid,ba_str):
        if(len(ba_str) > BLOK_SIZE):
            return False
        bid = self.blocks_out.popitem()
        print(bid)

        blok = self.getblok(padid,bid[1][0],0)
  
        el = bytearray()
        for a in range(0,len(ba_str)):
            el.append(ba_str[a] ^ blok[a])

        #Destroyblok(padid,bid[1][2])
        mack = hmac.new(bid[1][1],ba_str,HASHFUNC)

  

        return (pack(">Q",bid[0]), el, mack.digest())

    def decryptblock(self,ba_str):
        padid = unpack(">Q",ba_str[:8])[0]
        print(padid)
        if(padid in self.blocks_in):
            print("Block " + str(padid) + " found")
        else:
            print("Invalid block")
            return False

        blok = self.getblok(0,self.blocks_in[padid][0],1)

        el = bytearray()
        for a in range(0,len(ba_str)-40):
            el.append(ba_str[8+a] ^ blok[a])

        mack = hmac.new(self.blocks_in[padid][1],el,HASHFUNC)
                
        res = hmac.compare_digest(mack.digest(),ba_str[-32:])

        if(res == True):
            return el
        else: return False
        
