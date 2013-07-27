import transport_lan
import transport_udp4_direct
#import transport_serial
#import transport_bluetooth
#import transport_tcp_direct
#import transport_udp_storeforward
#import transport_http_storeforward
##import transport_nfc
##import transport_ar
##import transport_sms
##import transport_sbd
##import transport_torchat

friendly = {'lan':'Local Network','udp4':'Internet','bt':'Bluetooth','serial':'Serial'}

def parse_tpm(b_str,contact):
    pass

def disable_transport(tp_name):
    global transport_lan
    if(tp_name == 'lan'): transport_lan.Shutdown()
    del(transport_lan)

def send_msg(tp_name,mc,to_send,seqid):
    if(tp_name == 'lan'): transport_lan.send_msg(mc,seqid,to_send)

def send_ack(tp_name,mc,seqid):
    if(tp_name == 'lan'): transport_lan.send_ack(mc,seqid)
    
def send_bcast(tp_name,ch,msg):
    transport_lan.send_bcast_message(ch,msg)
