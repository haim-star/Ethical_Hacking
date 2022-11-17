#!/usr/bin/env pyton3

import subprocess
import optparse
import re


# ===============================
# = Read command from the user. =
# ===============================
def get_arg():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="interface to change its MAC address.")
    parser.add_option("-m", "--mac", dest="new_mac", help="new MAC address.")
    (opt, arg) = parser.parse_args()
    if not opt.interface or not opt.new_mac:
        parser.error("[-] Please specify an interface and a new mac address, use --help for more info.")
    return opt


# ========================
# = Change MAC address. =
# =============================
def change_mac(interface, new_mac):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


# =================================================
# = Get the Mac address of the  current interface =
# =================================================
def get_mac_address(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_add_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if not mac_add_search_result:
        print("[-] Can't find Mac address")
    else:
        return mac_add_search_result.group(0)


options = get_arg()
mac_address = get_mac_address(options.interface)
if mac_address:
    print("[!] Current MAC: " + mac_address)
    change_mac(options.interface, options.new_mac)
    new_mac_address = get_mac_address(options.interface)
    if not mac_address == new_mac_address:
        print("[+] Mac address was successfully changed to " + new_mac_address)
    else:
        print("[-] MAC address did not changed.")
