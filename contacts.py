import tp

from gi.repository import Gtk
from gi.repository import GdkPixbuf
from gi.repository import GLib


Contactlist = {}
Selected = -1

#Tree Store of contact list
gui_contactlist = Gtk.TreeStore(int,str,GdkPixbuf.Pixbuf)
sc_iter = gui_contactlist.append(None,[-2,"Saved (0)",None])
ld_iter = gui_contactlist.append(None,[-1,"Local (0)",None])
ua_iter = gui_contactlist.append(None,[-3,"Unreachable (0)",None])

#Gui items
Selbox = None
Sel_lbl = None
Nick_box = None
Builder = None

tp_l = Gtk.ListStore(str,int) #Info box transport list 
tp_combo = Gtk.ListStore(str,GdkPixbuf.Pixbuf) #Combo box select transport

#Pixbuf transports
pixbuf_lan = GdkPixbuf.Pixbuf.new_from_file_at_size("./graphics/lan.png",16,16)
pixbuf_bt = GdkPixbuf.Pixbuf.new_from_file_at_size("./graphics/bt.png",16,16)
pixbuf_udp4 = GdkPixbuf.Pixbuf.new_from_file_at_size("./graphics/wan.png",16,16)
transport_icon = {'lan':pixbuf_lan,'bt':pixbuf_bt,'udp4':pixbuf_udp4}


#Presence icons
pixbuf_grn = GdkPixbuf.Pixbuf.new_from_file_at_size("./graphics/grn.png",16,16)
pixbuf_red = GdkPixbuf.Pixbuf.new_from_file_at_size("./graphics/red.png",16,16)
pixbuf_orn = GdkPixbuf.Pixbuf.new_from_file_at_size("./graphics/orn.png",16,16)
pixbuf_unr = GdkPixbuf.Pixbuf.new_from_file_at_size("./graphics/unr.png",16,16)
presence_pb = {0:pixbuf_grn,1:pixbuf_orn,2:pixbuf_red,3:pixbuf_unr}
presence_text = {0:"Available",1:"Away",2:"Offline",3:"Unreachable"}
    
def wcd_close(w,e):
    w.hide()
    return True

def gui_showdetails(Treeview,path,view_column):
    global Builder
    Detailwindow = Builder.get_object("window_contact_details")
    Nick_lbl = Builder.get_object("wcd_nick")
    Presence_lbl = Builder.get_object("wcd_presence_status")
    
    Selection = Treeview.get_selection()
    (Gls,tree_iter) = Selection.get_selected()
    gv = Gls.get_value(tree_iter,0)

    if(gv> -1 ):
        print(Contactlist[gv].nick)
        #Populate window
        Nick_lbl.set_text(Contactlist[gv].nick)
        Presence_lbl.set_text("Status: " + presence_text[Contactlist[gv].presence])
        Detailwindow.show_all()

        #Transports treeview
        tp_l.clear()
        for a in Contactlist[gv].Transports: tp_l.append([a+ "\nnewline",868])
    
def nfid():
    if len(Contactlist) == 0: return 0
    for i in range(max(Contactlist) + 2):
        if(i in Contactlist):
                continue
        else:
                return i

def ui_remove(list_it,nfid):
    gui_contactlist.remove(list_it)
    ui_unselect(nfid)
    return False

def ui_unselect(nfid):
    global Selected
    if(Selected == nfid):
        Selected = -1
        Sel_lbl.set_text("No recipient selected")
        Sb = Selbox.get_selection()
        Sb.unselect_all()
        tp_combo.clear()
    return False

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
    def __init__(self,nick,presence):
        self.nick = nick
        self.list_it = None
        self.Transports = {}
        #self.Tsi = {} #Transport specific information
        self.Transport_info_string = {}
        self.saved = False     
        self.nfid = nfid()

        #Identifiers
        self.li = None
        self.gi = None
        self.si = None
        #0 = online,1=away,2=offline,3=unreachable
        self.presence = presence
        self.current_list = 0
        
        self.lastseen = 0 # Time
        self.timeout = 0

        Contactlist[self.nfid] = self # Add self to main contact list

        self.level = 5
        self.otp_id = -1
        self.enc_key = ""

        #self.Messages_incoming = {}
        #self.Messages_outgoing = {}

        self.Messages_pending = {}

    def save(self):
        if(self.saved == False):
            self.saved = True
            self.ui_update()

    def select(self):
        global Selected
        Selected = self.nfid
        GLib.idle_add(self.ui_settpl)

    def ui_settpl(self):    
        tp_combo.clear()
        for a in self.Transports:
            tp_combo.append([a,transport_icon[a]])
        
    def ui_set(self):
        #Select list to store contact on (saved / local detect / unreachable)
        if(self.saved == True and self.presence == 3): parent_iter = ua_iter
        elif(self.saved == True and self.presence != 3): parent_iter = sc_iter
        else:parent_iter = ld_iter

        if((self.current_list != 0) and (parent_iter != self.current_list)):
            ui_remove(self.list_it,self.nfid)
            self.list_it = None

        self.current_list = parent_iter        
        if(self.list_it): gui_contactlist[self.list_it] = [self.nfid,self.nick,presence_pb[self.presence]]
        else: self.list_it = gui_contactlist.append(parent_iter,[self.nfid,self.nick,presence_pb[self.presence]])       
        return False

    def ui_update(self):
        GLib.idle_add(self.ui_set)
        #if(self.nfid == Selected): GLib.idle_add(self.ui_settpl)
    
    def __del__(self):
        print("Delself")
        if(self.list_it != None):
            GLib.idle_add(ui_remove,self.list_it,self.nfid)
        
    def add_transport(self,transport,tpo):
        self.Transports[transport] = tpo
        
        
    def del_transport(self,transport):
        del self.Transports[transport]
        if(self.Transports == {}):
           self.presence = 3
           #Delete self if not saved and no transports remaining
           if(self.saved == True): self.ui_update()
           else: self.tibetan_monk()
        else:
            if(self.nfid == Selected): GLib.idle_add(self.ui_settpl)
        #Only store&forwards = Red
        #Direct transport available = Do nothing
       
    def tibetan_monk(self):
        print("Tibetan monk")
        if(self.nfid == Selected): GLib.idle_add(tp_combo.clear)        
        del(Contactlist[self.nfid])

def contact_by_li(li):
    for ctact in Contactlist:
        if(Contactlist[ctact].li == li): return Contactlist[ctact].nfid
    return -1

def all_with_transport(tp_name):
    lst = []
    for ctact in Contactlist:
        if('lan' in Contactlist[ctact].Transports): lst.append(ctact)
    return(lst)

