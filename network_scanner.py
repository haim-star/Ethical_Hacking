#!usr/bin/env python3
import optparse
import scapy.all as scapy


# ===============================
# = Read command from the user. =
# ===============================
def get_arg():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="an IP or range of IP's for search.")
    (opt, arg) = parser.parse_args()
    if not opt.target:
        parser.error("[-] Please specify a target IP, use --help for more info.")
    return opt.target


# ==============================================
# = Scan the network, return list of clients   =
# ==============================================
def scan(ip):
    arp_req = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_req_bro = broadcast / arp_req
    answered_list = scapy.srp(arp_req_bro, timeout=1, verbose=False)[0]

    clients_list = []
    for element in answered_list:
        clients_list.append({"ip": element[1].psrc, "mac": element[1].hwsrc})
    return clients_list


# ==============================================
# = Print list of clients IP and MAC addresses =
# ==============================================
def print_clients_list(client_list):
    print("---------------------------------------------------")
    print("    IP\t\t\t    MAC Address")
    print("---------------------------------------------------")
    for element in client_list:
        print(element["ip"] + "\t\t" + element["mac"])
        print("...............................................")


target = get_arg()
if target:
    clients = scan(target)
    print_clients_list(clients)
