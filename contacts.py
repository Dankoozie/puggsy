from gi.repository import Gtk
from random import randint
gui_contactlist = Gtk.ListStore(str,int)
Contactlist = {}

Selected = -1



#Gui items
Selbox = None
Sel_lbl = None

def nfid():
    if len(Contactlist) == 0: return 0
    for i in range(max(Contactlist) + 2):
        if(i in Contactlist):
                continue
        else:
                return i

# Contact class
# autodel
#
#
#

class Message_in:
    def __init__(self,mc,contents,transport):
        self.time_received = 0
        self.time_sent = 0
        self.timeout = 0
        self.mc = None
        self.transport = ""
        self.security = 0
        self.contents = 0
        self.multipart = ()
        self.seqid = 0
        
class Contact:
    def __init__(self):
        self.nick = ""
        self.list_it = None
        self.Transports = {}
        self.autodel = True     
        self.nfid = nfid()
        Contactlist[self.nfid] = self

        #self.Messages_incoming = {}
        #self.Messages_outgoing = {}
    def __del__(self):
        global Selected
        print("Delself")
        gui_contactlist.remove(self.list_it)
        if(self.nfid == Selected):
            Sel_lbl.set_text("No recipient selected")
            Selected = -1
            
    def add_transport(self,transport,key):
        self.Transports[transport] = key
        
    #def del_transport(self,transport):
    #   del self.Transports[transport]
    #  if(self.autodel and (not self.Transports)): del(self)

    def set_nick(self,nickname):
        self.nick = nickname
        if(self.list_it): gui_contactlist[self.list_it] = [nickname, self.nfid]
        else: self.list_it = gui_contactlist.append([nickname,self.nfid])

class Self_contact:
    def __init__(self,nickname):
        self.nick = nickname
        
Myself = Self_contact("Gorbitchoff")
