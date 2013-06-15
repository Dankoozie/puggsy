from gi.repository import Gtk
from gi.repository import GdkPixbuf
from gi.repository import GLib

gui_contactlist = Gtk.ListStore(int,str,GdkPixbuf.Pixbuf)
tp_l = Gtk.ListStore(str,int)

Contactlist = {}
Selected = -1

#Gui items
Selbox = None
Sel_lbl = None
Nick_box = None
Builder = None


#Presence icons
pixbuf_grn = GdkPixbuf.Pixbuf.new_from_file_at_size("./graphics/grn.png",16,16)
pixbuf_red = GdkPixbuf.Pixbuf.new_from_file_at_size("./graphics/red.png",16,16)
pixbuf_orn = GdkPixbuf.Pixbuf.new_from_file_at_size("./graphics/orn.png",16,16)
pixbuf_unr = GdkPixbuf.Pixbuf.new_from_file_at_size("./graphics/orn.png",16,16)
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
    print(Contactlist[gv].nick)

    #Populate window
    Nick_lbl.set_text(Contactlist[gv].nick)
    Presence_lbl.set_text("Status: " + presence_text[Contactlist[gv].presence])
    
    Detailwindow.show_all()

    #Transports treeview
    tp_l.clear()
    for a in Contactlist[gv].Transports:
        tp_l.append([a+ "\nnewline",Contactlist[gv].Transports[a]])
    
def nfid():
    if len(Contactlist) == 0: return 0
    for i in range(max(Contactlist) + 2):
        if(i in Contactlist):
                continue
        else:
                return i

def ui_remove(list_it):
    gui_contactlist.remove(list_it)
    return False

def ui_unselect():
    Sel_lbl.set_text("No recipient selected")
    Sb = Selbox.get_selection()
    Sb.unselect_all()
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
    def __init__(self):
        self.nick = ""
        self.list_it = None
        self.Transports = {}
        self.Transport_info_string = {}
        self.autodel = True     
        self.nfid = nfid()

        #0 = online,1=away,2=offline,3=unreachable
        self.presence = 0
        self.lastseen = 0 # Time

        Contactlist[self.nfid] = self

        self.level = 5
        self.otp_id = -1
        self.enc_key = ""

        #self.Messages_incoming = {}
        #self.Messages_outgoing = {}

        self.Messages_pending = {}
        
    def ui_nick(self):
        if(self.list_it): gui_contactlist[self.list_it] = [self.nfid,self.nick,presence_pb[self.presence]]
        else: self.list_it = gui_contactlist.append([self.nfid,self.nick,presence_pb[self.presence]])
        return False

    def ui_update(self):
        GLib.idle_add(self.ui_nick)
    
    def __del__(self):
        global Selected
        print("Delself")
        GLib.idle_add(ui_remove,self.list_it)
        
        if(self.nfid == Selected):
            Selected = -1
            GLib.idle_add(ui_unselect)
            
    def add_transport(self,transport,key):
        self.Transports[transport] = key
        
    #def del_transport(self,transport):
    #   del self.Transports[transport]
    #  if(self.autodel and (not self.Transports)): del(self)

