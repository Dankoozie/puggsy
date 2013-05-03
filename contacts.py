from gi.repository import Gtk
from random import randint
gui_contactlist = Gtk.ListStore(str,int)
Contactlist = {}
Selected = 0

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

class Contact:
    def __init__(self):
        self.nick = ""
        self.list_it = None
        self.Transports = {}
        self.autodel = True     
        self.nfid = nfid()
        Contactlist[self.nfid] = self
            
    def __del__(self):
        print("Delself")
        gui_contactlist.remove(self.list_it)

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
