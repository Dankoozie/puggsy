import pickle

from socket import gethostname
from random import randint
from os.path import isfile

__sf = "./setts/myself.pickle"

def save():
    fl = open(__sf,'wb')
    pickle.dump(Myself,fl)
    fl.close()

def gen_uid(size):
    g = b''
    for i in range(size):
        g = g + bytes([randint(0,255)])
    return g

class Self_contact:
    
    def __init__(self,nickname):
        self.nick = nickname
        self.presence = 0
        #Nick_box.set_text(nickname)

        self.p_uid = gen_uid(24)
        self.l_uid = gen_uid(24)
        self.s_uid = ""
        
        self.Transports = {}
        
    def transportstring(self):
        #Use pickle for now
        return pickle.dumps(self.transports)
    

if(not isfile(__sf)):
    Myself = Self_contact(gethostname())
    print("Generating new contact..")
else:
    print("Loading contact from file..")
    fl = open(__sf,'rb')
    Myself = pickle.load(fl)
    fl.close()
