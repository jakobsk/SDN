from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0

from ryu.lib.packet import packet
from ryu.lib.packet import ethernet


class L2Switch(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]


    def __init__(self, *args, **kwargs):
        super(L2Switch, self).__init__(*args, **kwargs)



    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        dp = msg.datapath
        ofp = dp.ofproto
        ofp_parser = dp.ofproto_parser

        pkt = packet.Packet(msg.data)
        eth = pkt[0]
        dst_mac = eth.dst

        if eth.protocol_name != 'ethernet':
            #We should not receive non-ethernet packets,
            #as these are dropped at the switch
            self.logger.warning('Received unexpected packet:')
            self.logger.warning(str(pkt))
            return


        self.logger.info('Received ethernet packet')

        if eth.ethertype == 2054:
            #this is an ARP packet
            #flood this kind of packets
            self.logger.info('Packet ethertype is ARP')
            self.logger.info('Flooding all ports on switch')

            actions = [ofp_parser.OFPActionOutput(ofp.OFPP_FLOOD)]
            out = ofp_parser.OFPPacketOut(datapath=dp, buffer_id=msg.buffer_id,in_port=msg.in_port, actions=actions)
            dp.send_msg(out)

        if eth.ethertype == 2048:
            #We should not receive non-IPv4 packets,
            #as these are dropped at the switch
            self.logger.info('Packet ethertype is IPv4')
            
            ip = pkt[1]

            if ip.proto == 0x01:
                self.logger.info('Packet IP protocol is ICMP')
                #need to block this if the IP address destination is that of H1
                #h1 has IP addr = 10.0.0.1
                if ip.dst == "10.0.0.1" and ip.identification==0:
                    self.logger.info('Blocked ICMP towards h1')
                    return
                else:
                    #Floods this as well..
                    actions = [ofp_parser.OFPActionOutput(ofp.OFPP_FLOOD)]
                    out = ofp_parser.OFPPacketOut(datapath=dp, buffer_id=msg.buffer_id,in_port=msg.in_port, actions=actions)
                    dp.send_msg(out)
       	            self.logger.info('Ping is flooded by the switch')