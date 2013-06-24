from socket import *
import threading
import contacts, struct, time, random
import messages



from myself import Myself

transport_trusted = False

Myself.Transports['udp4'] = ('86.43.88.90',10892)

class udp4_contact():
    def __init__(self,addr,port):
        self.addr = addr
        self.port = port    

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(('',10892))

listen_running = True


def process_unsecuredmsg(addr,packet):
    pass

def process_received(addr,data):
    pack_switch = {85:process_unsecuredmsg}
    print("Incoming! ", addr, data)

class listen(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.recvd = 0
    def run(self):
        while listen_running:
            data, addr = sock.recvfrom(1024)
            process_received(addr, data)

listener = listen()
listener.start()
