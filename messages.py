import sys
sys.path.insert(0,'./fivebit/') #Get rid of this later when fivebit is a real lib

from gi.repository import Gtk,Pango,GLib
import contacts
import notification
import fivebit
import time
import tp

from random import randint

lastprint = ()

tb = None
Mainwindow = None

Inbox = {}
Pending = [] #Contacts with pending messages
Sentbox = {}
Archived = {}



# ----------- GUI STUFF HERE -----------

buffy = Gtk.TextBuffer()
tag_in1 = buffy.create_tag("in1",foreground="#989898",weight=400)
tag_in2 = buffy.create_tag("in2",foreground="#900000",weight=600)
tag_in3 = buffy.create_tag("in3",foreground="#900000",weight=400)
tag_in4 = buffy.create_tag("in4",foreground="#000000",weight=400)

tag_out1 = buffy.create_tag("out1",foreground="#2071ae",weight=600)
tag_out2 = buffy.create_tag("out2",foreground="#2071ae",weight=400)

tag_bcast1 = buffy.create_tag("bcast1",foreground="#eace15",weight=600)
tag_bcast2 = buffy.create_tag("bcast2",foreground="#eace15",weight=400)

def msg_out_box(dest,contents,transport):
    enditer = buffy.get_end_iter()
    buffy.insert_with_tags(enditer,"\n" + time.strftime("[%H:%M:%S]"),tag_in1)
    buffy.insert_with_tags(enditer," Recipient: " + dest,tag_out1)
    buffy.insert_with_tags(enditer," (via " + tp.friendly[transport] +")\n",tag_out2)
    buffy.insert_with_tags(enditer,contents + "\n",tag_in4)
    tb.scroll_to_mark(buffy.get_insert(),0,False,0.5,0.5)

def msg_to_box(nick,contents,transport):
    enditer = buffy.get_end_iter()
    buffy.insert_with_tags(enditer,"\n" + time.strftime("[%H:%M:%S]"),tag_in1)
    buffy.insert_with_tags(enditer," Sender: " + nick,tag_in2)
    buffy.insert_with_tags(enditer," (via " + tp.friendly[transport] +")\n",tag_in3)
    buffy.insert_with_tags(enditer,contents + "\n",tag_in4)
    tb.scroll_to_mark(buffy.get_insert(),0,False,0.5,0.5)

def msg_dots_out(contents):
    enditer = buffy.get_end_iter()
    buffy.insert_with_tags(enditer,"... ",tag_out2)
    buffy.insert_with_tags(enditer,contents + "\n",tag_in4)

def msg_dots_in(contents):
    enditer = buffy.get_end_iter()
    buffy.insert_with_tags(enditer,"... ",tag_in2)
    buffy.insert_with_tags(enditer,contents + "\n",tag_in4)


# ----------- END GUI STUFF -----------



def gen_seqid(mc):
    sp = contacts.Contactlist[mc].Messages_pending
    for i in range(0,65535):
        if(not (i in sp)): return i

def process_ack(maincontact,transport,seqid):
    mc = contacts.Contactlist[maincontact]
    if(seqid in mc.Messages_pending):
        del(mc.Messages_pending[seqid])
        print("Message sequence " + str(seqid) + " delivered")
    else: print("[BOGUS]: Message identifier invalid")

def process_broadcast_message(tp,ch,nick,msg):
    #No idle add
    enditer = buffy.get_end_iter()
    buffy.insert_with_tags(enditer,time.strftime("[%H:%M:%S]"),tag_in1)
    buffy.insert_with_tags(enditer," LAN Broadcast: " + nick + ": ",tag_bcast1)
    buffy.insert_with_tags(enditer,msg + "\n\n",tag_in4)
    tb.scroll_to_mark(buffy.get_insert(),0,False,0.5,0.5)

def process_message(Msg_obj,compression = True):
    global lastprint
    #tx = "Message from: " + contacts.Contactlist[Msg_obj.mc].nick + " Transport: " + Msg_obj.transport + "\n" + str(Msg_obj.contents,'UTF-8') + "\n\n"

    if(compression == True):
        Msg_obj.contents = fivebit.decompress(Msg_obj.contents)

    #Use "..." if the message is sent or received from the same person
    if (Msg_obj.mc,Msg_obj.transport) != lastprint:
        GLib.idle_add(msg_to_box,contacts.Contactlist[Msg_obj.mc].nick,Msg_obj.contents,Msg_obj.transport)
        lastprint = (Msg_obj.mc,Msg_obj.transport)
    else: GLib.idle_add(msg_dots_in,Msg_obj.contents)


    #Send receipt
    tp.send_ack("lan",Msg_obj.mc,Msg_obj.seqid)

    #Notify
    #notification.sys_beep()
    #Mainwindow.set_urgency_hint(True)
    
def send_message(maincontact,transport,sec,body,compression = True):
    global lastprint


    if(compression == True):
        to_send = fivebit.compress(body)
    else:
        to_send = bytes(body,'UTF-8')


    if not (maincontact in contacts.Contactlist):
        logging.warning("Contact not found in contact list, not sending message")
        return False

    
    seqid = gen_seqid(maincontact)
    contacts.Contactlist[maincontact].Messages_pending[seqid] = body      
    tp.send_msg(transport,contacts.Contactlist[maincontact],to_send,seqid)

    #Use "..." if the message is sent or received from the same person   
    if (maincontact,transport) != lastprint:
        GLib.idle_add(msg_out_box,contacts.Contactlist[maincontact].nick,body,transport)
        lastprint = (maincontact,transport)
    else: GLib.idle_add(msg_dots_out,body)


class Msg_in:
    def __init__(self):
        pass
    


        
