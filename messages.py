from gi.repository import Gtk,Pango,GLib
import contacts
import transport_lan
import notification
import fivebit
import time
import tp

from random import randint

tb = None
Mainwindow = None

Inbox = {}
Pending = [] #Contacts with pending messages
Sentbox = {}
Archived = {}

buffy = Gtk.TextBuffer()
tag_in1 = buffy.create_tag("in1",foreground="#989898",weight=400)
tag_in2 = buffy.create_tag("in2",foreground="#900000",weight=600)
tag_in3 = buffy.create_tag("in3",foreground="#900000",weight=400)
tag_in4 = buffy.create_tag("in4",foreground="#000000",weight=400)

tag_out1 = buffy.create_tag("out1",foreground="#2071ae",weight=600)
tag_out2 = buffy.create_tag("out2",foreground="#2071ae",weight=400)

def msg_out_box(dest,contents,transport):
    enditer = buffy.get_end_iter()
    buffy.insert_with_tags(enditer,time.strftime("[%H:%M:%S]"),tag_in1)
    buffy.insert_with_tags(enditer," Recipient: " + dest,tag_out1)
    buffy.insert_with_tags(enditer," (via " + tp.friendly[transport] +")\n",tag_out2)
    buffy.insert_with_tags(enditer,contents + "\n\n",tag_in4)
    tb.scroll_to_mark(buffy.get_insert(),0,False,0.5,0.5)

def msg_to_box(nick,contents,transport):
    enditer = buffy.get_end_iter()
    buffy.insert_with_tags(enditer,time.strftime("[%H:%M:%S]"),tag_in1)
    buffy.insert_with_tags(enditer," Sender: " + nick,tag_in2)
    buffy.insert_with_tags(enditer," (via " + tp.friendly[transport] +")\n",tag_in3)
    buffy.insert_with_tags(enditer,contents + "\n\n",tag_in4)
    tb.scroll_to_mark(buffy.get_insert(),0,False,0.5,0.5)

def gen_seqid(mc):
    sp = contacts.Contactlist[mc].Messages_pending
    for i in range(0,65535):
        if(not (i in sp)): return i

def send_ack(Msg_obj):
    transport_lan.send_ack(Msg_obj.mc,Msg_obj.seqid)

def process_ack(maincontact,transport,seqid):
    mc = contacts.Contactlist[maincontact]
    if(seqid in mc.Messages_pending):
        del(mc.Messages_pending[seqid])
        print("Message sequence " + str(seqid) + " delivered")
    else: print("[BOGUS]: Message identifier invalid")

def process_message(Msg_obj,compression = True):
    #tx = "Message from: " + contacts.Contactlist[Msg_obj.mc].nick + " Transport: " + Msg_obj.transport + "\n" + str(Msg_obj.contents,'UTF-8') + "\n\n"

    if(compression == True):
        Msg_obj.contents = fivebit.decompress(Msg_obj.contents)

    GLib.idle_add(msg_to_box,contacts.Contactlist[Msg_obj.mc].nick,Msg_obj.contents,Msg_obj.transport)
    #Send receipt
    send_ack(Msg_obj)

    #Notify
    #notification.sys_beep()
    #Mainwindow.set_urgency_hint(True)
    
def send_message(maincontact,transport,sec,body,compression = True):

    if(compression == True):
        to_send = fivebit.compress(body)
    else:
        to_send = bytes(body,'UTF-8')

    
    if not (maincontact in contacts.Contactlist): return False
    seqid = gen_seqid(maincontact)
    contacts.Contactlist[maincontact].Messages_pending[seqid] = body
    if(transport == "lan"):      
        transport_lan.sendmsg(contacts.Contactlist[maincontact],to_send,seqid)
    elif(transport == "udp4"):
        transport_udp4_direct.sendmsg(contacts.Contactlist[maincontact],to_send,seqid)

    msg_out_box(contacts.Contactlist[maincontact].nick,body,transport)
    
class Msg_in:
    def __init__(self):
        pass
    


        
