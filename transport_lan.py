transport_trusted = True

from socket import *
import threading
import contacts, struct, time
import binascii
import messages,tp

from myself import Myself

first_broadcast = True

lan_contacts = {}

#Set up socket stuff
sock = socket(AF_INET6, SOCK_DGRAM)
bcast_addr = "ff02::1"
bcast_port = 49091
listen_port = 49091
bcast_time = 15
bcast_remove_factor = 3.1
bcast_running = True
listen_running = True
sock.bind(('',listen_port))

lan_uid = Myself.l_uid
Myself.Transports['lan'] = 1



def nfid_lan():
    if len(lan_contacts) == 0: return 0
    for i in range(max(lan_contacts) + 2):
        if(i in lan_contacts):
                continue
        else:
                return i

def peer_exists(uid):
    for i in lan_contacts:
        if(lan_contacts[i].b_uid == uid): return True
    return False
        
def peer_by_uid(uid):
    for i in lan_contacts:
        if(lan_contacts[i].b_uid == uid): return i
    return -1

class lancontact():
    def __init__(self,nick,addr,port,uid,status):
        self.nfid = None
        self.b_nick = nick
        self.b_addr = addr
        self.b_port = port
        self.b_uid = uid
        self.b_status = status
        self.b_lastrcvd = time.time()
        self.b_created = time.time()
        self.maincontact = -1
        
    def update_maincontact(self):
        #Create if not present
        if(self.maincontact == -1):
            mc = contacts.Contact()
            self.maincontact = mc.nfid

        contacts.Contactlist[self.maincontact].nick = str(self.b_nick,'UTF-8')
        contacts.Contactlist[self.maincontact].presence = self.b_status
        contacts.Contactlist[self.maincontact].ui_update()
        print("Status: ",self.b_status)
                   
    def addself(self):
        self.nfid = nfid_lan()
        lan_contacts[self.nfid] = self
        self.update_maincontact()
        contacts.Contactlist[self.maincontact].add_transport("lan",self.nfid)
        
    def __del__(self):
        if(self.maincontact != -1):
            ctd = contacts.Contactlist[self.maincontact]
            ctd.del_transport("lan")
            if(ctd.saved == False and (ctd.Transports == {})):
                del contacts.Contactlist[self.maincontact]
        print("Delself - Transport")


#Process LAN presence broadcast packet ('B<lan_uid><nickname>')    
def process_broadcast(addr,packet):
    uid = packet[3:27]
    interval = packet[1]
    #Flags (lsb=presence,1=bcast_request)
    flags = int(packet[2])
    status = flags & 1
    bcast_request = flags & 2
    
       
    nick = packet[27:]
    address = addr[0]
    port = addr[1]

    peer = peer_by_uid(uid)

    
    curcontact = (nick,address,port,uid)

    #Ignore packets from self 
    if(uid == lan_uid): return

    print("Incoming broadcast\n Nick:" + str(nick,'UTF-8') + "\nUID: " + str(binascii.hexlify(uid),'utf-8'))
    if not peer_exists(uid):
       #print("New contact discovered")
       Contactobject = lancontact(nick,address,port,uid,status)
       Contactobject.addself()
    else:
        existing_peer = peer_by_uid(uid)
        lan_contacts[existing_peer].b_nick = nick
        lan_contacts[existing_peer].b_addr = address
        lan_contacts[existing_peer].b_port = port
        lan_contacts[existing_peer].b_lastrcvd = time.time()
        lan_contacts[existing_peer].b_status = status
        lan_contacts[existing_peer].update_maincontact()
        
    if(bcast_request): bcast_send() # Notify new peer that you are around

#Process Unsecured LAN message('M<sender lan_uid><message>')        
def process_unsecuredmsg(addr,packet):
    peer = peer_by_uid(packet[1:25])
    print("Unsec msg incoming")
    if(peer in lan_contacts):
        #Attributes of received message
        Msg = contacts.Message_in(lan_contacts[peer].maincontact,packet[27:],"lan")
        Msg.time_received = time.time()
        Msg.timeout = 255
        Msg.security = 0
        Msg.seqid = struct.unpack("H",packet[25:27])[0]
        print(Msg.seqid)
        messages.process_message(Msg)
    else: print("[BOGUS]: Message received from unknown peer")

#Process 'sign off' packet
def process_signoff(addr,packet):
    lan_id = packet[1:25]
    peer = peer_by_uid(lan_id)
    if(peer in lan_contacts):
        #Possible 'peer = 0 problem'
        del(lan_contacts[peer])
        print("Peer signing off")


def process_transport_list(addr,packet):
    peer = peer_by_uid(packet[1:25])
    if(peer in lan_contacts):
        print(packet[25:])
        depickle = packet[25:]
        

def process_info(addr,packet):
    return True

def process_securedmsg(addr,packet):
    return True
    
#Handles incoming UDP packet
def process_received(addr, packet):
    pack_switch = {65:process_ack,
                   66:process_broadcast,
                   73:process_info,
                   83:process_securedmsg,
                   84:process_transport_list,
                   85:process_unsecuredmsg,
                   89:process_signoff}

    try:
        pack_switch[int(packet[0])](addr,packet)
    except KeyError:
        print("[BOGUS]: Invalid start byte " + str(int(packet[0])))
    
#Process incoming delivery receipt        
def process_ack(addr,packet):
    seqid = struct.unpack("H",packet[25:27])[0]
    lan_id = packet[1:25]
    peer = peer_by_uid(lan_id)
    if(peer != -1):
        messages.process_ack(lan_contacts[peer].maincontact,"lan",seqid)
    else: print("[BOGUS]: Delivery report (peer does not exist)")
    
#Send single presence broadcast (for use when one is received)
def bcast_send():
        global first_broadcast
        flags = ( (int(first_broadcast) << 1) + int(Myself.presence) ) 
    
        print("My status: ", Myself.presence)
        hdr = struct.pack("BBB",66,bcast_time,flags)
        sock.sendto(hdr + lan_uid + bytes(Myself.nick,'UTF-8'),(bcast_addr,bcast_port))    
        first_broadcast = False

def bcast():
    if(bcast_running):
        checktimeouts()
        bcast_send()
        threading.Timer(bcast_time,bcast).start()
    

def send_unsecuredmsg(lc,seq,msg):
    hdr = struct.pack("B",85) + lan_uid + struct.pack("H",seq) + msg
    if(lan_contacts[lc]):
            print("Sending unsec msg \n Addr:" + lan_contacts[lc].b_addr +"\n Port:" + str(lan_contacts[lc].b_port))
            sock.sendto(hdr,(lan_contacts[lc].b_addr,lan_contacts[lc].b_port))


def send_ack(mc,seq):
    lc = contacts.Contactlist[mc].Transports['lan']
    hdr = struct.pack("B",65) + lan_uid + struct.pack("H",seq)
    if(lan_contacts[lc]):
        print("Sending ACK for message")
        sock.sendto(hdr,(lan_contacts[lc].b_addr,lan_contacts[lc].b_port))

def sendmsg(mc,msg,seqid):
    lc = mc.Transports['lan']
    send_unsecuredmsg(lc,seqid,msg)

def checktimeouts():
    tdel = []
    for lc in lan_contacts:   
        if((time.time() - lan_contacts[lc].b_lastrcvd) > (bcast_time * bcast_remove_factor)):
            tdel.append(lc)
    for lc in tdel: del(lan_contacts[lc])


def Shutdown():
    global bcast_running,listen_running
    bcast_running = False
    listen_running = False
    #Tell other clients you are going offline
    sock.sendto(struct.pack("B",89) + lan_uid,(bcast_addr,bcast_port))

    
class listen(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.recvd = 0
    def run(self):
        while listen_running:
            data, addr = sock.recvfrom(1024)
            process_received(addr, data)
bcast()
listener = listen()
listener.start()
