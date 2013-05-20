from socket import *
import threading
import contacts, struct, time, random
import binascii
import messages

lan_contacts = {}

#Set up socket stuff
sock = socket(AF_INET6, SOCK_DGRAM)
lsock = socket(AF_INET6, SOCK_DGRAM)
bcast_addr = "ff02::1"
bcast_port = 49091
listen_port = 49091
bcast_time = 15
bcast_remove_factor = 3.1
bcast_running = True
listen_running = True
sock.bind(('',listen_port))

def gen_lan_uid():
    g = b''
    for i in range(24):
        g = g + bytes([random.randint(0,255)])
    return g

lan_uid = gen_lan_uid()


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
    return False

class lancontact():
    def __init__(self,nick,addr,port,uid):
        self.nfid = None
        self.b_nick = nick
        self.b_addr = addr
        self.b_port = port
        self.b_uid = uid
        self.b_lastrcvd = time.time()
        self.b_created = time.time()
        self.autodel = True
        self.maincontact = -1

        
    def update_maincontact(self):
        #Create if not present
        if(self.maincontact == -1):
            mc = contacts.Contact()
            self.maincontact = mc.nfid

        contacts.Contactlist[self.maincontact].set_nick(str(self.b_nick,'UTF-8'))
                   
    def addself(self):
        self.nfid = nfid_lan()
        lan_contacts[self.nfid] = self
        self.update_maincontact()
        contacts.Contactlist[self.maincontact].add_transport("lan",self.nfid)
        
    def __del__(self):
        if(self.maincontact != -1):
            ctd = contacts.Contactlist[self.maincontact]
            del(ctd.Transports["lan"])
            if(ctd.autodel and (ctd.Transports == {})):
                del contacts.Contactlist[self.maincontact]
        print("Delself - Transport")
    
def process_broadcast(addr,packet):
    uid = packet[2:26]
    interval = packet[1]
    nick = packet[26:]
    address = addr[0]
    port = addr[1]

    curcontact = (nick,address,port,uid)

    #Ignore packets from self 
    if(uid == lan_uid): return

    print("Incoming broadcast\n Nick:" + str(nick,'UTF-8') + "\nUID: " + str(binascii.hexlify(uid),'utf-8'))
    if not peer_exists(uid):
       #print("New contact discovered")
       Contactobject = lancontact(nick,address,port,uid)
       Contactobject.addself()
       bcast_nothread() # Notify new peer that you are around
    else:
        existing_peer = peer_by_uid(uid)
        lan_contacts[existing_peer].b_nick = nick
        lan_contacts[existing_peer].b_addr = address
        lan_contacts[existing_peer].b_port = port
        lan_contacts[existing_peer].b_lastrcvd = time.time()
        lan_contacts[existing_peer].update_maincontact()
        #print("Existing contact found")
    
def process_unsecuredmsg(addr,packet):
    peer = peer_by_uid(packet[1:25])
    print("Unsec msg incoming")
    if(lan_contacts[peer].b_uid == packet[1:25]):

        #Attributes of received message
        Msg = contacts.Message_in(lan_contacts[peer].maincontact,packet[27:],"lan")
        Msg.time_received = time.time()
        Msg.timeout = 255
        Msg.security = 0
        Msg.seqid = struct.unpack("H",packet[25:27])
        
        messages.process_message(Msg)
        

def process_received(addr, packet):
    #Process broadcast packet
    #print("Packet received")
    if(packet[0] == 66): process_broadcast(addr,packet)
    if(packet[0] == 85): process_unsecuredmsg(addr,packet)                  
    if(packet[0] == 89):
        lan_id = packet[1:25]
        peer = peer_by_uid(lan_id)
        if(peer and (lan_contacts[peer].nfid != lan_uid)):
            #Possible 'peer = 0 problem'
            print("Peer found - " + str(peer))
            del(lan_contacts[peer])
        print("Peer signing off")
        
    if(packet[0] == 65):
        print("Acknowledged: ")
        

    

def bcast_nothread():
        hdr = struct.pack("BB",66,bcast_time)
        sock.sendto(hdr + lan_uid + bytes(contacts.Myself.nick,'UTF-8'),(bcast_addr,bcast_port))    

def bcast():
    if(bcast_running):
        checktimeouts()
        hdr = struct.pack("BB",66,bcast_time)
        sock.sendto(hdr + lan_uid + bytes(contacts.Myself.nick,'UTF-8'),(bcast_addr,bcast_port))
        threading.Timer(bcast_time,bcast).start()
    

def send_unsecuredmsg(lc,seq,msg):
    hdr = struct.pack("B",85) + lan_uid + struct.pack("H",seq) + bytes(msg,'UTF-8')
    if(lan_contacts[lc]):
            print("Sending unsec msg \n Addr:" + lan_contacts[lc].b_addr +"\n Port:" + str(lan_contacts[lc].b_port))
            sock.sendto(hdr,(lan_contacts[lc].b_addr,lan_contacts[lc].b_port))


def send_ack(lc,seq):
    hdr = struct.pack("B",65) + lan_uid + struct.pack("H",seq)
    if(lan_contacts[lc]):
        print("Sending ACK for message")
        sock.sendto(hdr,(lan_contacts[lc].b_addr,lan_contacts[lc].b_port))

def sendmsg(mc,msg):
    lc = mc.Transports['lan']
    send_unsecuredmsg(lc,0,msg)

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
