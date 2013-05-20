from gi.repository import Gtk
from gi.repository import GLib
from random import randint
from socket import gethostname

gui_contactlist = Gtk.ListStore(str,int)


Contactlist = {}


Selected = -1



#Gui items
Selbox = None
Sel_lbl = None
Nick_box = None

def nfid():
    if len(Contactlist) == 0: return 0
    for i in range(max(Contactlist) + 2):
        if(i in Contactlist):
                continue
        else:
                return i

def ui_remove(list_it):
    gui_contactlist.remove(list_it)



class Message_in:
    def __init__(self,mc,contents,transport):
        self.time_received = 0
        self.time_sent = 0
        self.timeout = 0
        self.mc = mc
        self.transport = transport
        self.security = 0
        self.contents = contents
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

    def ui_nick(self):
        if(self.list_it): gui_contactlist[self.list_it] = [self.nick, self.nfid]
        else: self.list_it = gui_contactlist.append([self.nick,self.nfid])
        return False

    def ui_removeself(self):
        gui_contactlist.remove(self.list_it)
        return False
        
    def __del__(self):
        global Selected
        print("Delself")
        GLib.idle_add(ui_remove,self.list_it)
        
        if(self.nfid == Selected):
            Sel_lbl.set_text("No recipient selected")
            print("GAh")
            Selected = -1
            
    def add_transport(self,transport,key):
        self.Transports[transport] = key
        
    #def del_transport(self,transport):
    #   del self.Transports[transport]
    #  if(self.autodel and (not self.Transports)): del(self)

    def set_nick(self,nickname):
        self.nick = nickname
        GLib.idle_add(self.ui_nick)

class Self_contact:
    def __init__(self,nickname):
        self.nick = nickname
        #Nick_box.set_text(nickname)
        

Myself = Self_contact(gethostname())
